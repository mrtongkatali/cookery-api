<template lang="pug">
div
  div.overlay-preview.preview-img(v-if="picDialog.show")
    i.simple-icon-close.preview-close(@click="closePreview")
    img(:src="_fullUrlRef(form.identityProofImage, 480)")
  div#regMenu
    home-menu(:backEnabled="true", themeColor="white", :enableListLink="true")
    //- div.register-form(style="min-height:90vh")
  div.body-holder
    div.mx-3.pt-2
      h5.font-weight-normal.text-black.mb-1 {{ $t('business.extended_details') }}
      b-form#BoStep5Form(data-vv-scope="BoStep5Form", autocomplete="off")
        b-form-group(:label="$t('business.gst')", class="muted-placeholder")
          b-form-input(type="text", id="gstRegNo" v-model="form.gstRegNo", :placeholder="$t('business.gst_placeholder')", name="gstRegNo", maxlength="50", class="left input-line input-gray", @click.stop="_scrollTo('#gstRegNo', 500, null)")
          small.error.text-danger(v-if="errors.has('gstRegNo', 'BoStep5Form')") {{ errors.first('gstRegNo', 'BoStep5Form') }}
        b-form-group(:label="$t('business.select_proof')", class="muted-placeholder")
          multiselect(
            v-model="form.identityProofType",
            track-by="id",
            label="title",
            :options="proofType",
            :searchable="false",
            name="proof"
          )
          small.error.text-danger(v-if="errors.has('proof', 'BoStep5Form')") {{ errors.first('proof', 'BoStep5Form') }}

        template(v-if="form.identityProofImage")
          b-form-group(label="", class="muted-placeholder margin-t-27")
            div.w-100
              i.simple-icon-close.remove-photo(@click="removePhoto")
              div.uploaded-product(:style="{ backgroundImage : 'url(' + form.identityProofImage + ')' }", @click="showPicDialog")

        template(v-if="!form.identityProofImage")
          span.title-page {{ $t('business.upload_id_photo') }}
          uploaderWrapper.mb-5(:tips="$t('business.upload_tip')", @onImageUploaded="onImageUploaded", @onImageUploading="onImageUploading")
    div.mx-3
      b-button.btn-shadow.w-100(variant="primary", size="md", @click="formSubmit", :disabled="hasPendingUploads")
        span {{ $t('business.continue') }}

      b-button.mt-2.btn-shadow.w-100(variant="primary", size="md", @click="formSubmit('save')")
        span {{ $t('business.save_exit') }}
    br.clear
</template>
<script>
import { mapActions, mapGetters } from 'vuex'
import { Validator } from 'vee-validate'
import { RunnerService } from '@/api'
import moment from 'moment'
import { map, each } from 'lodash/collection'
import { indexOf } from 'lodash/array'
import Multiselect from 'vue-multiselect'
import 'vue-multiselect/dist/vue-multiselect.min.css'
const dictionary = {
  custom: {
    gstRegNo: {
      required: 'GST Number is required.'
    },
    proof: {
      required: 'ID Proof Type is required.'
    }
  }
}

Validator.localize('en', dictionary)
export default {
  name: 'business-register-step5',
  data () {
    return {
      topBanner: require(`@/assets/static/login/top-banner.jpg`),
      form: {
        gstRegNo: null,
        identityProofType: null,
        identityProofImage: null
      },
      picDialog: {
        show: false
      },
      proofType: [
        { id: `Voter's ID`, title: `Voter's ID` },
        { id: 'Passport', title: 'Passport' },
        { id: 'Aadhar Card', title: 'Aadhar Card' },
        { id: 'Driving License', title: 'Driving License' },
        { id: `Owner’s PAN card photo`, title: `Owner’s PAN card photo` }
      ],
      isDirty: false,
      imgUploadingCount: 0
    }
  },
  components: {
    homeMenu: () => import('@/components/home-menu'),
    uploaderWrapper: () => import('@/components/Widgets/ImageUploaderWrapper'),
    Multiselect
  },
  mounted () {
    this._initializeNotchTemplate('#fff', 'default')
    if (this.getStep3Identity) {
      this.form = this.getStep3Identity
    }

    window.scrollTo(0, 0)
  },
  watch: {
    form: {
      deep: true,
      handler: 'setDirtyForm'
    },
    isDirty: {
      deep: true,
      handler: 'autoSave'
    }
  },
  computed: {
    hasPendingUploads () {
      return (this.imgUploadingCount > 0 ? true : null)
    },
    ...mapGetters({
      getStep3Identity: 'getStep3Identity',
      Step0: 'getStep0',
      getStep1: 'getStep1',
      getStep2: 'getStep2',
      getStep3: 'getStep3'
    })
  },
  methods: {
    onImageUploading (value) {
      if (value) this.imgUploadingCount++
      else this.imgUploadingCount--
    },
    autoSave () {
      if (this.isDirty) {
        setTimeout(() => {
          this.setStep3Identity(this.form)
          this.isDirty = false
        }, 5000)
      }
    },
    setDirtyForm () {
      this.isDirty = true
    },
    ...mapActions([
      'setStep3Identity',
      'clearSteps'
    ]),
    showPicDialog () {
      this.picDialog.show = true
    },
    closePreview () {
      this.picDialog.show = false
    },
    removePhoto () {
      this.form.identityProofImage = null
    },
    onImageUploaded (fsRef) {
      this.form.identityProofImage = this.assetsURL(fsRef)
      this.imgUploadingCount = 0
    },
    async formSubmit (save) {
      let isValid = await this.$validator.validateAll('BoStep5Form')
      console.log('form', this.form)
      if (save === 'save' && isValid) {
        try {
          let payload = {
            // step 1 data
            description: this.getStep1.description,
            state: null,
            city: null,
            zip: this.getStep1.zip,
            additionalAddressDetails: this.getStep1.additionalAddressDetails,
            fullAddress: this.getStep1.fullAddress,
            lat: this.getStep1.lat,
            lon: this.getStep1.lon,
            businessLogo: this.getStep1.businessLogo,
            // step 2 data
            categories: this.getStep2.businessCategory && this.getStep2.businessCategory.length > 0 ? map(this.getStep2.businessCategory, 'title') : [],
            images: this.getStep2.images,
            workingHours: {
              startHour: 0,
              startMinute: 0,
              endHour: 0,
              endMinute: 0,
              days: {
                1: false,
                2: false,
                3: false,
                4: false,
                5: false,
                6: false,
                7: false
              }
            },
            // step 3 data
            // images: this.getStep3.images,
            writeUp: this.getStep3.writeUp,
            keywords: this.getStep3.keywords && this.getStep3.keywords.length > 0 ? map(this.getStep3.keywords, 'title') : [],
            traffic: {
              averageCustomer: this.getStep3.averageCustomers
            },
            additionalData: {
              averageSale: this.getStep3.averageSale
            },
            ageGroup: {
              groups: this.getStep3.ageGroup && this.getStep3.ageGroup.length > 0 ? map(this.getStep3.ageGroup, 'id') : []
            },
            gender: this.getStep3.gender,
            // step 3 identity data
            identityProofType: this.form.identityProofType ? this.form.identityProofType.id : null,
            gstRegNo: this.form.gstRegNo,
            identityProofImage: this.form.identityProofImage
          }
          if (this.getStep2.businessStartTime &&
            this.getStep2.businessStartTime.hasOwnProperty('hh') &&
            this.getStep2.businessStartTime.hasOwnProperty('mm') &&
            this.getStep2.businessStartTime.hasOwnProperty('a') &&
            this.getStep2.businessEndTime &&
            this.getStep2.businessEndTime.hasOwnProperty('hh') &&
            this.getStep2.businessEndTime.hasOwnProperty('mm') &&
            this.getStep2.businessEndTime.hasOwnProperty('a')
          ) {
            let now = moment().format('M-D-Y')
            payload.workingHours.startHour = parseInt(moment(`${now} ${this.getStep2.businessStartTime.hh}:${this.getStep2.businessStartTime.mm} ${this.getStep2.businessStartTime.a}`).format('HH'))
            payload.workingHours.startMinute = parseInt(moment(`${now} ${this.getStep2.businessStartTime.hh}:${this.getStep2.businessStartTime.mm} ${this.getStep2.businessStartTime.a}`).format('mm'))
            payload.workingHours.endHour = parseInt(moment(`${now} ${this.getStep2.businessEndTime.hh}:${this.getStep2.businessEndTime.mm} ${this.getStep2.businessEndTime.a}`).format('HH'))
            payload.workingHours.endMinute = parseInt(moment(`${now} ${this.getStep2.businessEndTime.hh}:${this.getStep2.businessEndTime.mm} ${this.getStep2.businessEndTime.a}`).format('mm'))
          }
          let days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
          each(days, (day, val) => {
            let hasDay = indexOf(this.getStep2.businessDays, day)
            if (hasDay >= 0) {
              let item = hasDay + 1
              payload.workingHours.days[item] = true
            }
          })
          console.log('payload', payload)
          await RunnerService.updateBusiness(this.Step0.id, payload)
          this.clearSteps()
          this.$router.push({ name: 'business-users-list' })
        } catch (e) {
          console.log(`e`, e)
          this.showDialogNotification(`error`, `Something went wrong`)
        }
      } else if (isValid) {
        this.setStep3Identity(this.form)
        this.$router.push({ name: 'step-4' })
      }
    }
  }
}
</script>
