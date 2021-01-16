<template lang="pug">
div
  div#regMenu
    home-menu(:backEnabled="true", themeColor="white", :enableListLink="true")
    //- div.register-form(style="min-height:90vh")
  div.body-holder
    div.mx-3.pt-2
      b-form#BoStep3Form(data-vv-scope="BoStep3Form", autocomplete="off")
        b-form-group(:label="`${$t('business.about')} *`", class="muted-placeholder")
          b-form-textarea.input-line.input-gray-textarea(no-resize, :placeholder="$t('business.about_business')", v-model="form.writeUp", name="writeUp")
          small.error.text-danger(v-if="errors.has('writeUp', 'BoStep3Form')") {{ errors.first('writeUp', 'BoStep3Form') }}
        b-form-group(:label="`${$t('business.keywords')} *`", class="muted-placeholder")
          multiselect(
            v-model="form.keywords",
            :tag-placeholder="$t('business.new_tag')",
            track-by="id",
            label="title",
            :options="listKeywords",
            :taggable="true",
            :multiple="true",
            @tag="addTag",
            name="keywords"
          )
          small.error.text-danger(v-if="errors.has('keywords', 'BoStep3Form')") {{ errors.first('keywords', 'BoStep3Form') }}

        span.title-page {{ $t('business.target_demograp') }}
        div
          b-form-group(:label="$t('business.age_group')", class="muted-placeholder")
            multiselect(
              v-model="form.ageGroup",
              :multiple="isMultiple",
              track-by="id",
              label="title",
              :placeholder="$t('business.select_age_group')",
              :options="ageGroupV2",
              :searchable="false",
              name="ageGroup"
            )
            small.error.text-danger(v-if="errors.has('ageGroup', 'BoStep3Form')") {{ errors.first('ageGroup', 'BoStep3Form') }}

          b-form-group(:label="$t('business.gender')", class="muted-placeholder")
            multiselect(
              v-model="form.gender",
              :placeholder="$t('business.select_gender')",
              :show-labels="false",
              :options="genderList",
              :searchable="false",
              name="gender"
            )
            small.error.text-danger(v-if="errors.has('gender', 'BoStep3Form')") {{ errors.first('gender', 'BoStep3Form') }}
          br
          span#estimates.title-page {{ $t('business.estimate_day') }}
          b-form-group(:label="$t('business.average_number_customers')", class="muted-placeholder")
            b-form-input(type="number", id="estimatesPerDay" v-model="form.averageCustomers", :placeholder="$t('business.enter_average_number_customers')", name="averageCustomers", maxlength="50", class="input-line input-gray", @click.stop="_scrollTo('#estimatesPerDay', 500, null)")
            small.error.text-danger(v-if="errors.has('averageCustomers', 'BoStep3Form')") {{ errors.first('averageCustomers', 'BoStep3Form') }}

          b-form-group(:label="$t('business.sale_total')", class="muted-placeholder")
            b-form-input(type="text", v-model="currency", :disabled="true", :placeholder="$t('business.currency')", name="currency", maxlength="1", class="input-line currency-input ")
            b-form-input(type="number", v-model="form.averageSale", :placeholder="$t('business.enter_average_number')", name="averageCustomers", maxlength="50", class="input-line input-gray price-input", @click.stop="_scrollTo('#estimatesPerDay', 500, null)")
            small.error.text-danger(v-if="errors.has('averageSale', 'BoStep3Form')") {{ errors.first('averageSale', 'BoStep3Form') }}
    div.mx-3
      b-button.btn-shadow.w-100(variant="primary", size="md", @click="formSubmit")
        span {{ $t('business.continue') }}

      b-button.mt-2.btn-shadow.w-100(variant="primary", size="md", @click="formSubmit('save')")
        span {{ $t('business.save_exit') }}
    br.clear
</template>
<script>
import { mapActions, mapGetters } from 'vuex'
import { RunnerService } from '@/api'
import { Validator } from 'vee-validate'
import moment from 'moment'
import { find, map, each } from 'lodash/collection'
import { indexOf } from 'lodash/array'
import Multiselect from 'vue-multiselect'
import 'vue-multiselect/dist/vue-multiselect.min.css'
const dictionary = {
  custom: {
    ageGroup: {
      required: 'Age Group is required.'
    },
    gender: {
      required: 'Gender is required.'
    },
    averageCustomers: {
      required: 'Average Customer is required.'
    },
    averageSale: {
      required: 'Average Sale is required.'
    },
    writeUp: {
      required: 'About is required.'
    }
  }
}

Validator.localize('en', dictionary)
export default {
  name: 'business-register-step3',
  data () {
    return {
      isMultiple: true,
      genderList: ['Both', 'Male', 'Female'],
      ageGroup: ['Everyone', 'Below 18', 'Age 18-24', 'Age 25-34', 'Age 35-44', 'Age 45-54', 'Age 55-64', 'Age 65 or above'],
      currency: '₹',
      form: {
        ageGroup: [],
        gender: 'Both',
        averageCustomers: 0,
        averageSale: 0,
        writeUp: null,
        keywords: []
      },
      listKeywords: [],
      ageGroupV2: [
        { id: 'agbelow18', title: 'Below 18' },
        { id: 'ag1824', title: 'Age 18-24' },
        { id: 'ag2534', title: 'Age 25-34' },
        { id: 'ag3544', title: 'Age 35-44' },
        { id: 'ag4554', title: 'Age 45-54' },
        { id: 'ag5564', title: 'Age 55-64' },
        { id: 'ag6500', title: 'Age 65 or above' },
        { id: 'everyone', title: 'Everyone' }
      ],
      isDirty: false
    }
  },
  components: {
    homeMenu: () => import('@/components/home-menu'),
    Multiselect
  },
  mounted () {
    this._initializeNotchTemplate('#fff', 'default')
    if (this.getStep3) {
      this.form = this.getStep3
    }

    window.scrollTo(0, 0)
  },
  watch: {
    'form.ageGroup' (newVal, oldVal) {
      let checkHasEveryone = find(this.form.ageGroup, { id: 'everyone' })
      if (checkHasEveryone && this.form.ageGroup.length > 1) {
        this.form.ageGroup = checkHasEveryone
        this.isMultiple = false
      } else {
        this.isMultiple = true
      }
    },
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
    ...mapGetters({
      getStep3: 'getStep3',
      getStep1: 'getStep1',
      getStep2: 'getStep2',
      Step0: 'getStep0'
    })
  },
  methods: {
    autoSave () {
      if (this.isDirty) {
        setTimeout(() => {
          console.log(`saved`)
          this.setStep3(this.form)
          this.isDirty = false
        }, 5000)
        console.log(`end test,`, this.isDirty)
      }
    },
    setDirtyForm () {
      console.log(`test,`, this.isDirty)
      this.isDirty = true
    },
    ...mapActions([
      'setStep3',
      'clearSteps'
    ]),
    addTag (newTag) {
      let tag = {
        id: newTag.substring(0, 2) + Math.floor((Math.random() * 10000000)),
        title: newTag
      }
      this.listKeywords.push(tag)
      this.form.keywords.push(tag)
    },
    async formSubmit (save) {
      let isValid = await this.$validator.validateAll('BoStep3Form')
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
            // images: this.form.images,
            writeUp: this.form.writeUp,
            keywords: this.form.keywords && this.form.keywords.length > 0 ? map(this.form.keywords, 'title') : [],
            traffic: {
              averageCustomer: this.form.averageCustomers
            },
            additionalData: {
              averageSale: this.form.averageSale
            },
            ageGroup: {
              groups: this.form.ageGroup && this.form.ageGroup.length > 0 ? map(this.form.ageGroup, 'id') : []
            },
            gender: this.form.gender
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
        this.setStep3(this.form)
        this.$router.push({ name: 'step-3-identity' })
      }
    },
    setAge (age) {
      this.form.ageGroup = age
    },
    setGender (gender) {
      this.form.gender = gender
    }
  }
}
</script>
