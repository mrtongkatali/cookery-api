<template lang="pug">
div.login-container#navRegistration
  div#regMenu
    home-menu(:backEnabled="true", themeColor="white", :enableListLink="true")
  image-uploader(:showDialogBox="showUploadDialog", :label="$t('business.how_photo')" @onDialogClose="onDialogClose", @onImageUploaded="onImageUploaded", @onImageUploading="onImageUploading")

  b-modal(id="devicePermissionDialog", ref="devicePermissionDialog", class="modal-long", hide-footer, hide-header, centered, no-close-on-esc, no-close-on-backdrop)
    //- div.text-center.text-center.mb-2
    //-   img(:src="bannerAPrompt", class="supportBanner")
    template(v-if="user.deviceAuthorizationStatus === 'PENDING_APPROVAL'")
      h5.text-muted.text-center.font-weight-bold For security purposes, your device has been under reviewed by the Go2Local team. Please come back later.
      div.mt-3.mb-2
        .d-flex.justify-content-between.align-items-center
          b-button.btn-shadow.w-gt(type="button", variant="info default", size="sm", @click.stop="$router.push({ name: 'more' })") {{ $t('business_owner.coin.step_1.prompt_button') }}

    template(v-else-if="user.deviceAuthorizationStatus === 'REJECTED'")
      h5.text-muted.text-center.font-weight-bold Device is not allowed to access this feature. Please contact Go2Local team.
      div.mt-3.mb-2
        .d-flex.justify-content-between.align-items-center
          b-button.btn-shadow.w-gt(type="button", variant="info default", size="sm", @click.stop="$router.push({ name: 'more' })") {{ $t('business_owner.coin.step_1.prompt_button') }}

    //- if no device uuid registered on user profile
    template(v-else-if="!user.deviceUuid && deviceInfo && deviceInfo.uuid")
      h5.text-muted.text-center.font-weight-bold Device must be registered first before you can access this feature. Please tap the register button to register your device.

      div.text-center.mt-4.font-weight-bold.h5 Your device UUID is
      div.text-center.font-weight-bold.h3 {{ deviceInfo.uuid }}

      div.mt-3.mb-2
        .d-flex.justify-content-between.align-items-center
          b-button.btn-shadow.w-gt(type="button", variant="info default", size="sm", @click.stop="registerDevice", :disabled="progress.deviceRegistration") {{ (progress.deviceRegistration ? 'Registering device ...' : 'Register Device') }}

    //- if no device uuid detected on phone
    template(v-else-if="!deviceInfo || !deviceInfo.uuid")
      h5.text-muted.text-center.font-weight-bold Unable to fetch your device uuid. Please check your phone settings and try again.

      div.mt-3.mb-2
        .d-flex.justify-content-between.align-items-center
          b-button.btn-shadow.w-gt(type="button", variant="info default", size="sm", @click.stop="$router.push({ name: 'more' })") Go Back

  div.body-holder(v-scroll:throttle="{fn: onScroll, throttle: 100 }", v-if="!loading")
    div.uploader-container.pt-2(@click="triggerUpload")
      div.uploadFiller.white-bg(v-if="!form.businessLogo")
        span.logo-filler {{ $t('business.upload_logo') }}
      div.uploadFiller(v-if="form.businessLogo", :style="{ backgroundImage : 'url(' + form.businessLogo + ')' }")
      i.simple-icon-camera.icon-camera
    div.mx-3
      h5.font-weight-normal.text-black.mb-1 {{ $t('business.basic_info') }}
      b-form#BoStep1(data-vv-scope="BoStep1", autocomplete="off")
        //- b-form-group(:label="`${$t('business.business_name')} *`", class="muted-placeholder")
          b-form-input(type="text", v-model="form.businessName", :placeholder="$t('business.enter_business_name')", name="businessName", v-validate.lazy="'required'", maxlength="50", class="input-line input-gray")
          small.error.text-danger(v-if="errors.has('businessName', 'BoStep1')") {{ errors.first('businessName', 'BoStep1') }}

        b-form-group(:label="`${$t('business.tagline')} *`", class="muted-placeholder")
          b-form-textarea.input-line.input-gray-textarea(no-resize, :placeholder="$t('business.enter_tagline')", v-model="form.description", name="businessDescription")
          //- small.error.text-danger(v-if="errors.has('businessDescription', 'BoStep1')") {{ errors.first('businessDescription', 'BoStep1') }}

        //- b-form-group(:label="`${$t('business.contact_person')} *`", class="muted-placeholder")
          b-form-input(type="text", v-model="form.contactPerson", :placeholder="$t('business.enter_contact_person')", name="contactPerson", class="input-line input-gray")
      //- making inputs outside b-form to exclude them from validateAll
      //- mobileInput(@onMobileChanged="triggerMobileChanged", :defaultMobileNo="form.ownerMobile", @onMobileCheck="onMobileCheck")
      b-form#BoStep11(data-vv-scope="BoStep11", autocomplete="off")
        //- addressAutocomplete(:countryRestriction="countryRestriction")
        //- b-form-group(:label="$t('business.business_address')", class="muted-placeholder")
          b-form-input(type="text", v-model="form.fullAddress", :placeholder="$t('business.enter_address')", name="fullAddress", v-validate.lazy="'required'", class="input-line input-gray")
          small.error.text-danger(v-if="errors.has('fullAddress', 'BoStep11')") {{ errors.first('fullAddress', 'BoStep11') }}
        b-form-group(:label="`${$t('business.location')} *`", class="muted-placeholder")
          location-selector(v-if="latLng && latLng.lat && latLng.lon && country && radiusInMeters", :lat="Number(latLng.lat)", :lon="Number(latLng.lon)", :radiusInMeters="Number(radiusInMeters)", @onUpdate="getMarkerPosition", :countryObj="country", @onAddressChanged="setAddress", @onAddressValidate="isAddressValid")
          span(v-else) {{ $t('business.unable_to_access') }}
        b-form-group(:label="`${$t('business.zip_code')} *`", class="muted-placeholder")
          b-form-input(type="number", v-model="form.zip", :placeholder="$t('business.enter_zip_code')", name="zipCode", maxlength="50", class="input-line input-gray", @click="_scrollTo('#BoStep11', 500, null)")
        b-form-group(:label="$t('business.additional_details')", class="muted-placeholder")
          b-form-textarea.input-line.input-gray-textarea(no-resize, :placeholder="$t('business.enter_additional_details')", v-model="form.additionalAddressDetails", name="additionalAddressDetails")
    div.mx-3
      b-button.btn-shadow.w-100(variant="primary", size="md", @click="formSubmit", :disabled="hasPendingUploads")
        span {{ $t('business.continue') }}

      b-button.mt-2.btn-shadow.w-100(variant="primary", size="md", @click="formSubmit('save')", :disabled="hasPendingUploads")
        span {{ $t('business.save_exit') }}
    br.clear
</template>
<script>
// import Vue from 'vue'
import { MiscService, AuthService, RunnerService } from '@/api'
import { mapActions, mapGetters } from 'vuex'
import { Validator } from 'vee-validate'
import { EventBus } from '@/utils'
const dictionary = {
  custom: {
    businessName: {
      required: 'Business Name is required.'
    },
    businessDescription: {
      required: `Tagline is required.`
    },
    zipCode: {
      required: `Zip Code is required`
    },
    fullAddress: {
      required: `Business Address is required`
    }
  }
}

Validator.localize('en', dictionary)
export default {
  name: 'business-register-step1',
  data () {
    return {
      user: {},
      deviceInfo: {},
      logoColored: require(`@/assets/static/logo/me_wala.png`),
      profileIcon: require(`@/assets/static/menu/icon-profile.png`),
      bannerAPrompt: require(`@/assets/static/support/support.png`),
      map: require(`@/assets/static/registration/map.png`),
      uploaderFiller: require(`@/assets/static/registration/profile.png`),
      form: {
        errors: [],
        businessLogo: null,
        businessName: null,
        description: null,
        ownerMobile: null,
        contactPerson: null,
        areaCode: null,
        countryObj: null,
        fullAddress: null,
        zip: null,
        additionalAddressDetails: null,
        lat: null,
        lon: null
      },
      // @NOTE: cleanup / test data
      // form: {
      //   errors: [],
      //   businessLogo: 'https://sme-dev-cdn.access.thebrainsyndicate.net/11124849-5a8f-4056-9048-addffa65173a.jpg',
      //   businessName: 'flyer test',
      //   description: 'flyer test',
      //   ownerMobile: '9645219913',
      //   contactPerson: 'flyer test',
      //   areaCode: null,
      //   countryObj: null,
      //   fullAddress: null,
      //   zip: '12345',
      //   additionalAddressDetails: 'flyer test',
      //   lat: null,
      //   lon: null
      // },
      isValidMobileNumber: false,
      isValidAddress: false,
      showUploadDialog: false,
      position: null,
      latLng: {
        lat: null,
        lon: null
      },
      countryRestriction: [],
      radiusInMeters: null,
      loading: true,
      isDirty: false,
      imgUploadingCount: 0,
      progress: {
        deviceRegistration: false
      }
    }
  },
  components: {
    homeMenu: () => import('@/components/home-menu'),
    addressSelector: () => import('@/components/Widgets/AddressSelector'),
    mobileInput: () => import('@/components/Widgets/MobileInput'),
    imageUploader: () => import('@/components/Widgets/ImageUploader'),
    locationSelector: () => import('@/components/Widgets/LocationSelector'),
    addressAutocomplete: () => import('@/components/Widgets/address-autocomplete')
  },
  mounted () {
    this.init()
    this._initializeNotchTemplate('#fff', 'default')
    if (this.getStep1 && this.getStep1.businessLogo) {
      this.isValidAddress = true
      this.form = this.getStep1
      this.latLng = {
        lat: this.getStep1.lat,
        lon: this.getStep1.lon
      }
      this.loading = false
    } else {
      /* eslint-disable no-undef */
      /* eslint-disable handle-callback-err */
      this.getLocationCoordinates().then((res) => {
        console.log(`[INFO] coords - `, res)
        this.latLng = {
          lat: (res && res.coords ? res.coords.latitude : null),
          lon: (res && res.coords ? res.coords.longitude : null)
        }
        this.form.lat = (res && res.coords ? res.coords.latitude : null)
        this.form.lon = (res && res.coords ? res.coords.longitude : null)
        this.loading = false
      }, (err) => {
        this.loading = false
        this.addNotification(`error filled`, `Notification`, this.$t('notification.location_unavailable'))
      })
    }

    if (this.latLng && this.latLng.lat && this.latLng.lon) {
      // if (this.form.countryObj)
      console.log(`country`, this.form.countryObj, this.latLng)
    }
    this.isDirty = false
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
      getStep0: 'getStep0',
      getStep1: 'getStep1',
      country: 'getCountry'
    })
  },
  methods: {
    async registerDevice () {
      // this.user = await AuthService.me()
      try {
        this.progress.deviceRegistration = true

        const payload = {
          deviceUuid: this.deviceInfo.uuid,
          deviceDetails: {
            model: this.deviceInfo.model,
            os: this.deviceInfo.platform,
            osVersion: this.deviceInfo.version
          }
        }

        await RunnerService.sendDeviceAuthorization(payload)
        this.user = await AuthService.me()

        this.progress.deviceRegistration = false
      } catch (e) {
        this.progress.deviceRegistration = false
        this.addNotification(`error filled`, `Oops!`, this._parseErrorRes(e))
      }
    },
    async init () {
      const settings = await MiscService.getKey('featureSettings')
      // if (settings && settings.value) {
      //   console.log(`xxx`, JSON.parse(settings.value))
      // }
      this.radiusInMeters = (settings && settings.value ? JSON.parse(settings.value)['radiusInMeters'] : 15)
      // this.user = await AuthService.me()
      // this.deviceInfo = (Vue.cordova && Vue.cordova.device ? Vue.cordova.device : {})
      //
      // if (
      //   (this.user && this.user.deviceAuthorizationStatus !== 'APPROVED') ||
      //   (!this.user || !this.user.deviceUuid)
      // ) {
      //   this.$refs['devicePermissionDialog'].show()
      // }
    },
    onImageUploading (value) {
      if (value) this.imgUploadingCount++
      else this.imgUploadingCount--
    },
    autoSave () {
      if (this.isDirty) {
        setTimeout(() => {
          this.setStep1(this.form)
          this.isDirty = false
        }, 5000)
      }
    },
    setDirtyForm () {
      this.isDirty = true
    },
    setImage () {
      this.form.businessLogo = this.assetsURL(`81fce1d3-d4d4-460c-8bbc-6fcf70b6bee0.jpg`)
    },
    ...mapActions([
      'setStep1',
      'clearSteps'
    ]),
    onScroll (e, position) {
      this.position = position
      if (this.position.scrollTop > 25) {
        document.getElementById('regMenu').classList.add('nav-scroll-border')
      } else {
        document.getElementById('regMenu').classList.remove('nav-scroll-border')
      }
    },
    isAddressValid (status) {
      this.isValidAddress = status
    },
    onMobileCheck (status) {
      this.isValidMobileNumber = status.isValid
    },
    async formSubmit (save) {
      this.errors.clear()

      let isFormValid = await this.$validator.validateAll('BoStep1')
      let isForm2Valid = await this.$validator.validateAll('BoStep11')
      // if (!this.form.businessLogo) {
      //   this.setImage()
      //   // this.showDialogNotification(`error`, `Business Logo is required`)
      // }

      EventBus.$emit('validate-address-selection')

      if (save === 'save' && isFormValid && isForm2Valid && this.isValidAddress) {
        try {
          let payload = {
            description: this.form.description,
            state: null,
            city: null,
            zip: this.form.zip,
            additionalAddressDetails: this.form.additionalAddressDetails,
            fullAddress: this.form.fullAddress,
            lat: this.form.lat,
            lon: this.form.lon,
            businessLogo: this.form.businessLogo
          }
          console.log('payload', payload)
          await RunnerService.updateBusiness(this.getStep0.id, payload)
          this.clearSteps()
          this.$router.push({ name: 'business-users-list' })
        } catch (e) {
          console.log(`e`, e)
          this.showDialogNotification(`error`, `Something went wrong`)
        }
      } else if (isFormValid && isForm2Valid && this.isValidAddress) {
        this.setStep1(this.form)
        console.log('this.form', this.form)
        this.$router.push({ name: 'step-2' })
      }
    },
    onImageUploaded (fsRef) {
      this.form.businessLogo = this.assetsURL(fsRef) // this.assetsUrl(`81fce1d3-d4d4-460c-8bbc-6fcf70b6bee0.jpg`)
      this.showUploadDialog = false
    },
    onDialogClose () {
      this.showUploadDialog = false
    },
    triggerUpload () {
      this.showUploadDialog = true
    },
    setAddress (address) {
      this.form.fullAddress = address
    },
    triggerMobileChanged (mobile) {
      this.form.countryObj = mobile
      this.form.ownerMobile = mobile.mobileNumber
      this.form.areaCode = mobile.mobileCode
    },
    triggerAddressChanged (address) {
      this.form.address = address
    },
    getMarkerPosition (position) {
      this.latLng = {
        lat: position.lat,
        lon: position.lng
      }
      this.form.lat = position.lat
      this.form.lon = position.lng
    }
  }
}
</script>
