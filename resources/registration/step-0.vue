<template lang="pug">
div.login-container#navRegistration
  div#regMenu
    home-menu(:backEnabled="true", themeColor="white", :enableListLink="true")

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

  div.body-holder.d-flex.flex-column.mh-100.my-0.pt-4(v-scroll:throttle="{fn: onScroll, throttle: 100 }", v-if="!loading")
    //- slide up
    div.slide-up.bg-white.mh-100.z-index-10(:class="showSlide ? 'show' : ''")
      div.d-flex.flex-column.mh-100.pt-5
        template(v-if="businesses")
          //- move the  close button on header if needed
          h4.mdi.mdi-close.text-right.mt-1.mr-2(@click="restartForm")
          div.text-center.text-center.mb-2
            img(:src="searchImg", height="150")
          h5.text-center.px-4.mt-1.font-weight-normal We have found #[strong {{ businesses.length }} business] #[br] and #[strong {{ countSimilar }} similar business]
          //- h3.text-muted.text-center.geoDialogText.line-height-20.px-4.mt-1(v-if="countSimilar > 0") Do you wish to create a new business for the same number?
          div.w-100.px-4.d-flex.flex-column(v-for="(biz, idx) in businesses", :key="idx")
            div.d-flex.border-bottom-grey.py-3
              div.mr-1
                img(:src="profileIcon", width="50px", height="50px").object-cover.radius-100
              div
                div
                  h5.mb-05.font-weight-normal.mr-2 {{ biz.businessName }}
                  p.lh-2.text-xsmall.mb-0 {{ biz.fullAddress }}
          div.mx-4.mt-auto.mb-2.pt-3
            .d-flex.justify-content-between.align-items-center
              b-button.btn-shadow.w-100.mr-2(type="button", variant="outline-primary" size="sm", @click.stop="restartForm") Cancel
              b-button.btn-shadow.w-100(type="button", variant="primary" size="sm", @click.stop="formSubmit") Continue
    div.mx-3.pt-2
      h5.font-weight-normal.text-black.mb-1 {{ $t('business.basic_info') }}
      b-form#BoStep1(data-vv-scope="BoStep1", autocomplete="off")
        b-form-group(:label="`${$t('business.business_name')} *`", class="muted-placeholder")
          b-form-input(type="text", v-model="form.businessName", :placeholder="$t('business.enter_business_name')", name="businessName", v-validate.lazy="'required'", maxlength="50", class="left input-line input-gray")
          small.error.text-danger(v-if="errors.has('businessName', 'BoStep1')") {{ errors.first('businessName', 'BoStep1') }}

        b-form-group(:label="`${$t('business.contact_person')} *`", class="muted-placeholder")
          b-form-input(type="text", v-model="form.contactPerson", :placeholder="$t('business.enter_contact_person')", name="contactPerson", class="left input-line input-gray")
      //- making inputs outside b-form to exclude them from validateAll
      mobileInput(@onMobileChanged="triggerMobileChanged", :defaultMobileNo="form.ownerMobile", @onMobileCheck="onMobileCheck")
      small.error.text-danger(v-if="isMobileEmpty").position-relative.top-minus-25 {{ $t('business.register_number_required') }}
    div.mx-3.mt-auto
      p.text-muted(v-if="sentRegkey") {{ $t('business.register_proceed_with_items') }}
      b-button.btn-shadow.w-100(variant="primary", size="md", @click="continueStep", v-if="sentRegkey")
        span {{ $t('business.continue') }}

      b-button.btn-shadow.w-100(variant="primary", size="md", @click="validateMobile", v-if="!sentRegkey", :disabled="!form.ownerMobile || !form.businessName || !form.contactPerson")
        span {{ $t('business.register_verify_number') }}
    br.clear
</template>
<script>
// import Vue from 'vue'
import { RunnerService, MiscService, AuthService } from '@/api'
import { mapActions, mapGetters } from 'vuex'
import { Validator } from 'vee-validate'
import { EventBus } from '@/utils'
import { filter } from 'lodash/collection'
const dictionary = {
  custom: {
    businessName: {
      required: 'Business Name is required.'
    },
    contactNo: {
      required: 'Mobile Number is required.'
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
  name: 'business-register-step0',
  data () {
    return {
      user: {},
      deviceInfo: {},
      progress: {
        deviceRegistration: false
      },
      showSlide: false,
      searchImg: require(`@/assets/static/dialog/search.png`),
      logoColored: require(`@/assets/static/logo/me_wala.png`),
      profileIcon: require(`@/assets/static/menu/icon-profile.png`),
      map: require(`@/assets/static/registration/map.png`),
      uploaderFiller: require(`@/assets/static/registration/profile.png`),
      form: {
        errors: [],
        id: null,
        businessName: null,
        description: null,
        ownerMobile: null,
        contactPerson: null,
        areaCode: null,
        countryObj: null,
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
      isMobileEmpty: false,
      sentRegkey: false,
      businesses: null
    }
  },
  components: {
    homeMenu: () => import('@/components/home-menu'),
    mobileInput: () => import('@/components/Widgets/MobileInput')
  },
  mounted () {
    this.init()
    this._initializeNotchTemplate('#fff', 'default')
    console.log('getStep0', this.getStep0)
    if (this.getStep0 && this.getStep0.businessName) {
      // this.isValidMobileNumber = true
      this.isValidAddress = true
      this.form = this.getStep0
      this.latLng = {
        lat: this.getStep0.lat,
        lon: this.getStep0.lon
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
        this.clearSteps()
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
    },
    'form.ownerMobile' (val, oldVal) {
      if (val !== oldVal) this.sentRegkey = false
    },
    isValidMobileNumber (val) {
      if (val) {
        this.checkBusiness()
      }
    }
  },
  computed: {
    countSimilar () {
      return filter(this.businesses, { businessName: this.form.businessName }).length
    },
    hasPendingUploads () {
      return (this.imgUploadingCount > 0 ? true : null)
    },
    ...mapGetters({
      getStep0: 'getStep0',
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
    restartForm () {
      this.form.contactPerson = null
      this.form.businessName = null
      this.form.ownerMobile = null
      this.isValidMobileNumber = false
      this.isMobileEmpty = true
      this.businesses = null
      // this.$refs['businessModal'].hide()
      this.showSlide = false
    },
    async validateMobile () {
      try {
        this.errors.clear()
        if (!this.form.ownerMobile) this.isMobileEmpty = true
        if (this.form.ownerMobile) {
          EventBus.$emit('validate-mobile-number')
          this.isMobileEmpty = false
        }
      } catch (e) {
        this.addNotification(`error filled`, `Oops`, this._parseErrorRes(e))
      }
    },
    async checkBusiness () {
      try {
        if (this.isValidMobileNumber) {
          this.businesses = await RunnerService.getBusinessByContactNumber({
            countryCode: this.form.areaCode,
            contactNo: this.form.ownerMobile
          })
          if (this.businesses.length > 0) {
            // this.$refs['businessModal'].show()
            this.showSlide = true
          } else {
            this.formSubmit()
          }
        }
      } catch (e) {
        this.addNotification(`error filled`, `Oops`, this._parseErrorRes(e))
      }
    },
    async init () {
      const settings = await MiscService.getKey('featureSettings')
      this.radiusInMeters = (settings && settings.value ? JSON.parse(settings.value)['radiusInMeters'] : 15)

      this.user = await AuthService.me()
      // this.deviceInfo = (Vue.cordova && Vue.cordova.device ? Vue.cordova.device : {})
      //
      // if (
      //   (this.user && this.user.deviceAuthorizationStatus !== 'APPROVED') ||
      //   (!this.user || !this.user.deviceUuid)
      // ) {
      //   this.$refs['devicePermissionDialog'].show()
      //   return
      // }
      //
      // if (this.getStep0 && this.getStep0 === this.form) this.sentRegkey = true
    },
    autoSave () {
      if (this.isDirty) {
        setTimeout(() => {
          this.setStep0(this.form)
          this.isDirty = false
        }, 5000)
      }
    },
    setDirtyForm () {
      this.isDirty = true
    },
    // setImage () {
    //   this.form.businessLogo = this.assetsURL(`81fce1d3-d4d4-460c-8bbc-6fcf70b6bee0.jpg`)
    // },
    ...mapActions([
      'setStep0',
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
    onMobileCheck (status) {
      console.log(`status`, status)
      this.isValidMobileNumber = status.isValid
      if (!this.isValidMobileNumber) this.addNotification('error filled', this.$t('mobileInput.invalid'))
    },
    async formSubmit () {
      if (this.countSimilar > 0) {
        this.form.businessName = null
        this.isValidMobileNumber = false
        // this.$refs['businessModal'].hide()
        this.showSlide = false
        this.businesses = null
        return
      }
      try {
        this.errors.clear()
        // if (!this.form.ownerMobile) this.isMobileEmpty = true
        // if (this.form.ownerMobile) {
        //   EventBus.$emit('validate-mobile-number')
        //   this.isMobileEmpty = false
        // } else {
        //   this.isValidMobileNumber = true
        // }

        let isFormValid = await this.$validator.validateAll('BoStep1')
        if (isFormValid && this.isValidMobileNumber) {
          let users = []
          if (this.form.ownerMobile && this.form.areaCode) {
            let owner = {
              countryCode: this.form.areaCode,
              contactNo: this.form.ownerMobile,
              rollType: 'OWNER'
            }
            users.push(owner)
          }
          console.log('form', this.form)
          let payload = {
            businessName: this.form.businessName,
            contactPerson: this.form.contactPerson,
            country2Code: this.form.countryObj.code,
            countryCode: this.form.areaCode,
            contactNo: this.form.ownerMobile,
            // lat: this.form.lat,
            // lon: this.form.lon,
            businessUsers: users,
            isDraft: true
          }
          // create new business
          console.log('payload', payload)
          let res = await RunnerService.createBusiness(payload)
          console.log('created business', res)
          // this.$refs['businessModal'].hide()
          this.showSlide = false
          // send regkey
          this.sendRegKey(res)
        }
      } catch (e) {
        this.addNotification(`error filled`, `Oops`, this._parseErrorRes(e))
      }
    },
    async sendRegKey (business) {
      console.log('sending key', business)
      try {
        if (business && business.currentStatus === 'DRAFT') {
          await RunnerService.resendRegKey(business.id)
          this.sentRegkey = true
          this.form.id = business.id
          this.setStep0(this.form)
        }
      } catch (e) {
        console.log(`e`, e)
        this.showDialogNotification(`error`, `Something went wrong`)
        this.sentRegkey = false
      }
    },
    continueStep () {
      this.$router.push({ name: 'step-1' })
    },
    // onDialogClose () {
    //   this.showUploadDialog = false
    // },
    // triggerUpload () {
    //   this.showUploadDialog = true
    // },
    // setAddress (address) {
    //   this.form.fullAddress = address
    // },
    triggerMobileChanged (mobile) {
      this.form.countryObj = mobile
      this.form.ownerMobile = mobile.mobileNumber
      this.form.areaCode = mobile.mobileCode
    }
    // triggerAddressChanged (address) {
    //   this.form.address = address
    // },
    // getMarkerPosition (position) {
    //   this.latLng = {
    //     lat: position.lat,
    //     lon: position.lng
    //   }
    //   this.form.lat = position.lat
    //   this.form.lon = position.lng
    // }
  }
}
</script>
