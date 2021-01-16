<template lang="pug">
div
  div.overlay-preview.preview-img(v-if="picDialog.show && picDialog.url")
    i.simple-icon-close.preview-close(@click="closePreview")
    img(:src="_fullUrlRef(picDialog.url, 480)")
  div
    div#regMenu
      home-menu(:backEnabled="true", themeColor="white", :enableListLink="true")
    image-uploader(:showDialogBox="showUploadDialog", :label="$t('business.how_photo')" @onDialogClose="onDialogClose", @onImageUploaded="onImageUploaded", @onImageUploading="onImageUploading")
    image-uploader2(:showDialogBox="showVideoUploadDialog", :label="$t('business.how_video')" @onDialogClose="onVideoDialogClose", @onVideoUploaded="onVideoUploaded", :uploaderMode="'video'", @loading="videoLoading")
    div.body-holder
      //- div.uploader-container(@click="triggerUpload")
        div.uploadFiller(:style="{ backgroundImage : 'url(' + uploaderFiller + ')' }")
        i.simple-icon-camera.icon-camera
      div.mx-3.pt-2
        h5.font-weight-normal.text-black.mb-1 {{ $t('business.basic_info') }}
        b-form#BoStep2(data-vv-scope="BoStep2", autocomplete="off")
          b-form-group(:label="`${$t('business.business_category')} *`", class="muted-placeholder", v-if="categories")
            multiselect(
              ref="multiSelect",
              v-model="form.businessCategory",
              :multiple="true",
              track-by="id",
              label="title",
              :placeholder="$t('business.select_categories')",
              :options="categories",
              :searchable="true",
              :deselect-label="$t('business.already_selected')",
              :allow-empty="false",
              name="businessCategory",
              @open="onSelect"
            )
              span(slot="noResult") {{ $t('mobileInput.invalid') }}
            small.error.text-danger(v-if="errors.has('businessCategory', 'BoStep2')") {{ errors.first('businessCategory', 'BoStep2') }}
          br
          b-form-group(:label="`${$t('business.business_hours')} *`", class="muted-placeholder")
            b-form-checkbox-group(v-model="form.businessDays", name="businessDays")
              div.day-container
                div.day(v-for="day in days", :key="day")
                  b-form-checkbox(:value="day", class="input-day")
                  span {{ day }}
              small.error.text-danger(v-if="errors.has('businessDays', 'BoStep2')") {{ errors.first('businessDays', 'BoStep2') }}
            div.hour-container
              div.start-container
                span {{ $t('shop.open') }}
                vue-timepicker(class="cs-timepicker", format="hh:mm a", :placeholder="$t('business.select_opening')", v-model="form.businessStartTime")
              div.end-container
                span {{ $t('shop.closes') }}
                vue-timepicker(class="cs-timepicker", format="hh:mm a", :placeholder="$t('business.select_closing')", v-model="form.businessEndTime")
            //- small.text-danger.text-center.d-block(v-if="hasTime") {{ $t('business.start_time_required') }}
          b-alert.mt-3.mb-3(show, variant='danger', v-if="form.errors.length > 0 && checkHasError('images')")
            p.alert-heading.strong
              i.pr-2.simple-icon-exclamation
              | {{ $t('business.upload_2_photos') }}
          b-form-group(:label="`${$t('business.upload_business_photos')} *`", class="muted-placeholder margin-t-27")
            div.upload-filler-container.d-flex
              div.col-4.px-0.border-right-grey(v-if="tempImages && tempImages.length > 0", v-for="(img, idx) in tempImages", :key="idx")
                img(:src="_fullUrlRef(img, 240)", @click="showPicDialog(img)").object-cover.w-100.h-120px
                i.simple-icon-close.text-danger.position-absolute.top-0.right-0.close-btn-with-bg.m-05(@click="removePic(idx)")

              template(v-if="tempImages && tempImages.length < 3")
                div.col-4.px-0.border-grey.d-flex.align-items-center.justify-content-center.h-120px(v-for="n in (3 - tempImages.length)", :key="`empty_${n}`", @click="triggerUpload")
                  i.mdi.mdi-plus.text-small(v-if="tempImages.length + n === 1") Cover Photo
                  h2.mb-0.iconsminds-add-file.text-secondary(v-else)
          span.title-page {{ $t('business.take_video') }}
          b-progress(v-if="videoUploading", :value="100", variant="success", :striped="true", animated)
          b-form-group(:label="$t('business.upload_video_clip')", class="muted-placeholder")
            div.video-container(@click="triggerVideoUpload")
              span.upload-text
                i.simple-icon-camera.left.icon-video
                span {{ $t('business.tap_to_record') }}
            div.video-container(v-if="form.businessVideo && !videoUploading")
              video(width="320", height="240", controls)
                source(:src="form.businessVideo", type="video/mp4")
      div.mx-3
        b-button.btn-shadow.w-100(variant="primary", size="md", @click="formSubmit", :disabled="videoUploading || hasPendingUploads")
          span {{ $t('business.continue') }}

        b-button.mt-2.btn-shadow.w-100(variant="primary", size="md", @click="formSubmit('save')", :disabled="hasPendingUploads")
          span {{ $t('business.save_exit') }}
      br.clear
</template>
<script>
import { mapActions, mapGetters } from 'vuex'
import { Validator } from 'vee-validate'
import Multiselect from 'vue-multiselect'
import { MiscService, RunnerService } from '@/api'
import { indexOf } from 'lodash/array'
import moment from 'moment'
import { each, map } from 'lodash/collection'
import VueTimepicker from 'vue2-timepicker'
import 'vue-multiselect/dist/vue-multiselect.min.css'
import 'vue2-timepicker/dist/VueTimepicker.css'
const dictionary = {
  custom: {
    businessCategory: {
      required: 'Business Category is required.'
    },
    theme: {
      required: `Theme is required`
    },
    businessDays: {
      required: `Business Days are required`
    }
  }
}

Validator.localize('en', dictionary)
export default {
  name: 'business-register-step2',
  data () {
    return {
      days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      categories: null,
      map: require(`@/assets/static/registration/map.png`),
      uploaderFiller: require(`@/assets/static/registration/profile.png`),
      videoUploading: false,
      form: {
        theme: null,
        errors: [],
        businessCategory: null,
        images: {
          hero: null,
          gallery: []
          // cleanup / test data
          // gallery: [
          //   'https://sme-dev-cdn.access.thebrainsyndicate.net/11124849-5a8f-4056-9048-addffa65173a.jpg',
          //   'https://sme-dev-cdn.access.thebrainsyndicate.net/11124849-5a8f-4056-9048-addffa65173a.jpg'
          // ]
        },
        businessVideo: '',
        // cleanup / test data
        // businessVideo: 'https://sme-dev-cdn.access.thebrainsyndicate.net/0ce3bb88-484c-4dec-8aa7-50e92987ce7d.mp4',
        businessDays: [],
        businessStartTime: {
          hh: '12',
          mm: '00',
          a: 'am'
        },
        businessEndTime: {
          hh: '12',
          mm: '00',
          a: 'am'
        }
      },
      tempImages: [],
      // cleanup / test data
      // tempImages: [
      //   'https://sme-dev-cdn.access.thebrainsyndicate.net/11124849-5a8f-4056-9048-addffa65173a.jpg',
      //   'https://sme-dev-cdn.access.thebrainsyndicate.net/11124849-5a8f-4056-9048-addffa65173a.jpg'
      // ],
      showUploadDialog: false,
      showVideoUploadDialog: false,
      position: null,
      uploadedImage: 'https://images.unsplash.com/photo-1558980664-10e7170b5df9?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2251&q=80',
      uploadedImage2: 'https://images.unsplash.com/photo-1582201943021-e8e5cb6dedc2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1924&q=80',
      uploadedImage3: 'https://images.unsplash.com/photo-1582487852212-c7ff8cf66bcb?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2250&q=80',
      picDialog: {
        show: false,
        url: null
      },
      isDirty: false,
      imgUploadingCount: 0
    }
  },
  components: {
    homeMenu: () => import('@/components/home-menu'),
    imageUploader: () => import('@/components/Widgets/ImageUploader'),
    imageUploader2: () => import('@/components/Widgets/ImageUploader'),
    Multiselect,
    VueTimepicker
  },
  mounted () {
    this._initializeNotchTemplate('#fff', 'default')
    this.init()
    if (this.getStep2) {
      // this.tempImages = []
      if (this.getStep2.images.hero) {
        this.tempImages.push(this.getStep2.images.hero)
      }

      if (this.getStep2.images.gallery && this.getStep2.images.gallery.length > 0) {
        each(this.getStep2.images.gallery, (img) => {
          this.tempImages.push(img.full)
        })
      }
      this.form = this.getStep2
    }

    if (this.tempVideo) {
      this.onVideoUploaded(this.tempVideo)
      this.updateCrashVideo(null)
    }
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
      getStep2: 'getStep2',
      getStep1: 'getStep1',
      Step0: 'getStep0',
      tempVideo: '_getCrashVideo'
    }),
    hasTime () {
      return (
        !this.form.businessStartTime ||
        !this.form.businessEndTime ||
        (this.form.businessStartTime && (!this.form.businessStartTime.hh || !this.form.businessStartTime.mm || !this.form.businessStartTime.a)) ||
        (this.form.businessEndTime && (!this.form.businessEndTime.hh || !this.form.businessEndTime.mm || !this.form.businessEndTime.a)) ||
        (this.form.businessStartTime && this.form.businessEndTime && this.form.businessStartTime.hh === this.form.businessEndTime.hh && this.form.businessStartTime.a === this.form.businessEndTime.a && this.form.businessStartTime.mm === this.form.businessEndTime.mm)
      )
    }
  },
  methods: {
    onImageUploading (value) {
      if (value) this.imgUploadingCount++
      else this.imgUploadingCount--
    },
    autoSave () {
      if (this.isDirty) {
        setTimeout(() => {
          this.setStep2(this.form)
          this.isDirty = false
        }, 5000)
      }
    },
    setDirtyForm () {
      this.isDirty = true
    },
    setImg () {
      this.tempImages.push(this.uploadedImage)
      if (!this.form.businessVideo) this.form.businessVideo = `https://file-examples.com/wp-content/uploads/2017/04/file_example_MP4_480_1_5MG.mp4`
    },
    onSelect () {
      const multiselect = this.$refs.multiSelect
      const input = multiselect.$refs.search

      if (input.style.display === 'none') {
        input.style.display = 'block'
        input.focus()
      }
    },
    ...mapActions([
      'setStep2',
      'clearSteps',
      'updateCrashVideo'
    ]),
    async init () {
      let response = await MiscService.getKey('category')
      this.categories = JSON.parse(response.value)
    },
    setCategory (cat) {
      this.form.businessCategory = cat
    },
    validateAssets () {
      this.form.errors = []
      if (this.tempImages.length < 2) {
        this.form.errors.push(`images`)
      }
      return this.form.errors.length === 0 // true no errors
    },
    checkHasError (field) {
      if (this.form.errors === 0) return false
      return indexOf(this.form.errors, field) >= 0
    },
    async formSubmit (save) {
      console.log('form', this.form)
      let isFormValid = await this.$validator.validateAll('BoStep2')
      // if (isFormValid && !this.hasTime) {
      if (isFormValid) {
        // this.tempImages.length = 3
        console.log('tempImages', this.tempImages)
        if (this.tempImages.length >= 1) {
          // get the first image
          this.form.images.hero = this.tempImages[0]
          this.form.images.gallery = []
          this.tempImages.splice(0, 1)
        }

        if (this.tempImages.length >= 1) {
          // get the remaining images and put it on gallery
          each(this.tempImages, (val) => {
            this.form.images.gallery.push({
              full: val
              // full: 'https://sme-dev-cdn.access.thebrainsyndicate.net/11124849-5a8f-4056-9048-addffa65173a.jpg'
            })
          })
          this.tempImages = []
        }
        if (save === 'save') {
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
              categories: this.form.businessCategory && this.form.businessCategory.length > 0 ? map(this.form.businessCategory, 'title') : [],
              images: this.form.images,
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
              }
            }
            if (this.form.businessStartTime &&
              this.form.businessStartTime.hasOwnProperty('hh') &&
              this.form.businessStartTime.hasOwnProperty('mm') &&
              this.form.businessStartTime.hasOwnProperty('a') &&
              this.form.businessEndTime &&
              this.form.businessEndTime.hasOwnProperty('hh') &&
              this.form.businessEndTime.hasOwnProperty('mm') &&
              this.form.businessEndTime.hasOwnProperty('a')
            ) {
              let now = moment().format('M-D-Y')
              payload.workingHours.startHour = parseInt(moment(`${now} ${this.form.businessStartTime.hh}:${this.form.businessStartTime.mm} ${this.form.businessStartTime.a}`).format('HH'))
              payload.workingHours.startMinute = parseInt(moment(`${now} ${this.form.businessStartTime.hh}:${this.form.businessStartTime.mm} ${this.form.businessStartTime.a}`).format('mm'))
              payload.workingHours.endHour = parseInt(moment(`${now} ${this.form.businessEndTime.hh}:${this.form.businessEndTime.mm} ${this.form.businessEndTime.a}`).format('HH'))
              payload.workingHours.endMinute = parseInt(moment(`${now} ${this.form.businessEndTime.hh}:${this.form.businessEndTime.mm} ${this.form.businessEndTime.a}`).format('mm'))
            }
            let days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            each(days, (day, val) => {
              let hasDay = indexOf(this.form.businessDays, day)
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
        } else {
          this.setStep2(this.form)
          this.$router.push({ name: 'business-theme-selection' })
        }
      }
    },
    async onImageUploaded (fsRef) {
      if (this.tempImages && this.tempImages.length < 3) {
        // this.form.images.gallery.push({
        //   full: this.assetsURL(fsRef)
        // })
        this.tempImages.push(this.assetsURL(fsRef))
      } else {
        this.addNotification(`error filled`, `Oops!`, this.$t('business.max_of_3'))
      }
    },
    videoLoading (state) {
      this.videoUploading = state
    },
    onVideoUploaded (fsRef) {
      this.form.businessVideo = null
      this.form.businessVideo = this.assetsURL(fsRef)
    },
    onDialogClose () {
      this.showUploadDialog = false
    },
    onVideoDialogClose () {
      this.showVideoUploadDialog = false
    },
    triggerUpload () {
      this.showUploadDialog = true
    },
    triggerVideoUpload () {
      this.showVideoUploadDialog = true
    },
    removePic (idx) {
      this.tempImages.splice(idx, 1)
    },
    showPicDialog (img) {
      this.picDialog.url = img
      this.picDialog.show = true
    },
    closePreview () {
      this.picDialog.url = null
      this.picDialog.show = false
    }
  }
}
</script>
