<template lang="pug">
div
  div#regMenu
    home-menu(:backEnabled="true", themeColor="white", :enableListLink="true")
  div.body-holder.pt-2
    div.mx-3
      div(v-if="isComplete").product-vertical
        h5.text-black.mb-1.text-center.summary-header {{ $t('business.ready_onboard') }}
        p.summary-description(v-if="isComplete") {{ $t('business.click_register') }}
        img.summary-banner(:src="summaryBanner")
      div(v-if="!isComplete")
        h5.font-weight-normal.text-black.mb-1 {{ $t('business.summary') }}
        p.caption {{ $t('business.looks_like') }}
        template
          p.caption {{ $t('business.to_complete') }}
          ul
            li(v-for="(field, idx) in fieldMissing", :key="idx") {{ field }}
      p.caption(v-if="this.user && (this.user.onBoardingType === 2 || this.user.onBoardingType === 'FLYER')") {{ $t('business.continue_to_enter') }}
      br
      div.mx-3
        b-button.btn-shadow.w-100.position-relative(variant="primary", size="md", @click="formSubmit", :disabled="isDisabled")
          b-spinner(small, v-if="isDisabled").button-loader.mr-2
          span(v-if="!isComplete") {{ $t('business.save_continue') }}
          span(v-if="isComplete") {{ $t('business.register') }}
</template>

<script>
/* eslint-disable */
import { mapActions, mapGetters } from 'vuex'
import { RunnerService, MiscService } from '@/api'
import { each, map } from 'lodash/collection'
import { indexOf } from 'lodash/array'
import moment from 'moment'
export default {
  name: 'registration-summary',
  data () {
    return {
      position: null,
      isComplete: false,
      isDisabled: false,
      fieldMissing: [],
      summaryBanner: require(`@/assets/static/registration/summary.png`)
    }
  },
  methods: {
    validateBusinessFields () {
      if ((this.getStep2.businessCategory && this.getStep2.businessCategory.length === 0) || !this.getStep2.businessCategory) this.fieldMissing.push(`Business Category`)
      // if (!this.getStep2.businessVideo) this.fieldMissing.push(`Business Video`)
      if (!this.getStep1.businessLogo) this.fieldMissing.push(`Business Logo`)
      if (!this.getStep1.fullAddress) this.fieldMissing.push(`Address`)
      if (!this.getStep0.contactPerson) this.fieldMissing.push(`Contact Person`)
      if (this.getStep2.images && (!this.getStep2.images.hero || (this.getStep2.images.gallery && this.getStep2.images.gallery.length === 0))) this.fieldMissing.push(`Business Photos (2 or more)`)
      if (!this.getStep0.ownerMobile) this.fieldMissing.push(`Contact Number`)
      if (!this.getStep1.description) this.fieldMissing.push(`Description`)
      if (!this.getStep2.theme) this.fieldMissing.push(`Theme`)
      if (!this.getStep1.zip) this.fieldMissing.push(`Zip`)
      // if (this.getStep3.ageGroup && this.getStep3.ageGroup.length === 0) this.fieldMissing.push(`Age Group`)
      // if (!this.getStep3.gender) this.fieldMissing.push(`Gender`)
      if (!this.getStep3.writeUp) this.fieldMissing.push(`About`)
      // if (!this.getStep3Identity.identityProofType) this.fieldMissing.push(`Identity Proof Type`)
      // if (!this.getStep3Identity.gstRegNo) this.fieldMissing.push(`GST Number`)
      // if (!this.getStep3Identity.identityProofImage) this.fieldMissing.push(`Identity Proof Image`)
      if (this.getStep3.keywords && this.getStep3.keywords.length === 0) this.fieldMissing.push(`Keywords`)
      if (this.getStep4.length === 0) this.fieldMissing.push(`Products (1 or more)`)
      if ((this.getStep2.businessStartTime &&
        (!this.getStep2.businessStartTime.hasOwnProperty('hh') ||
        !this.getStep2.businessStartTime.hasOwnProperty('mm') ||
        !this.getStep2.businessStartTime.hasOwnProperty('a'))) &&
        (this.getStep2.businessEndTime &&
        (!this.getStep2.businessEndTime.hasOwnProperty('hh') ||
        !this.getStep2.businessEndTime.hasOwnProperty('mm') ||
        !this.getStep2.businessEndTime.hasOwnProperty('a')))
      ) {
        this.fieldMissing.push(`Working Hours`)
      }

      this.isComplete = this.fieldMissing && this.fieldMissing.length === 0
    },
    async formSubmit () {
      try {
        this.isDisabled = true
        let products = []
        let categoriesList = await MiscService.getKey('productVectors')
        if (this.getStep4 && this.getStep4.length > 0) {
          each(this.getStep4, (prod) => {
            let gallery = []

            if (prod.images.length < 1) {
              let productVector = JSON.parse(categoriesList.value)[prod.category.toLowerCase()]
              let productVectorRandom = productVector[Math.floor(Math.random() * productVector.length)]
              gallery.push({
                full: productVectorRandom
              })
            } else {
              each(prod.images, (img) => {
                gallery.push({
                  full: img
                })
              })
            }
            let payload = {
              title: prod.title,
              category: prod.category,
              description: prod.description,
              price: prod.price ? prod.price : 0,
              size: prod.productSize,
              images: {
                gallery: gallery
              },
              weightInGrams: prod.weightInGrams
            }
            this.uploadProduct(payload)
          })
        }
        //
        // let users = []
        // if (this.getStep1.ownerMobile && this.getStep1.areaCode) {
        //   let owner = {
        //     countryCode: this.getStep1.areaCode,
        //     contactNo: this.getStep1.ownerMobile,
        //     rollType: 'OWNER'
        //   }
        //   users.push(owner)
        // }

        let payload = {
          businessName: this.getStep0.businessName,
          fullAddress: this.getStep1.fullAddress,
          description: this.getStep1.description,
          theme: this.getStep2.theme ? this.getStep2.theme.code : null,
          country2Code: this.getStep0.countryObj.code,
          countryCode: this.getStep0.areaCode,
          contactNo: this.getStep0.ownerMobile,
          contactPerson: this.getStep1.contactPerson,
          categories: this.getStep2.businessCategory && this.getStep2.businessCategory.length > 0 ? map(this.getStep2.businessCategory, 'title') : [],
          state: null,
          city: null,
          zip: this.getStep1.zip,
          additionalAddressDetails: this.getStep1.additionalAddressDetails,
          lat: this.getStep1.lat,
          lon: this.getStep1.lon,
          businessLogo: this.getStep1.businessLogo,
          ageGroup: {
            groups: this.getStep3.ageGroup && this.getStep3.ageGroup.length > 0 ? map(this.getStep3.ageGroup, 'id') : []
          },
          gender: this.getStep3.gender,
          // videoRec: this.getStep2.businessVideo,
          images: this.getStep2.images,
          writeUp: this.getStep3.writeUp,
          keywords: this.getStep3.keywords && this.getStep3.keywords.length > 0 ? map(this.getStep3.keywords, 'title') : [],
          // products: products,
          traffic: {
            averageCustomer: this.getStep3.averageCustomers
          },
          additionalData: {
            averageSale: this.getStep3.averageSale
          },
          // businessUsers: users,
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
          // isDraft: !this.isComplete,
          identityProofType: this.getStep3Identity.identityProofType ? this.getStep3Identity.identityProofType.id : null,
          gstRegNo: this.getStep3Identity.gstRegNo,
          identityProofImage: this.getStep3Identity.identityProofImage
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

        // let res = await RunnerService.createBusiness(payload)
        console.log('payload', payload)
        let res = await RunnerService.updateBusiness(this.getStep0.id, payload)

        if (this.user && (this.user.onBoardingType === 2 || this.user.onBoardingType === 'FLYER')) {
          res.isBizComplete = this.isComplete
          this._setBizDetails_(res)
          this.$router.push({ name: 'flyer-confirmation' })
        } else {
          let msg = this.$t('flyer.new_biz_registration')
          if (!this.isComplete) msg = this.$t('flyer.biz_draft')

          this.clearSteps()
          this.addNotification('success filled', this.$t('business.congrats'), msg)
          this.isDisabled = false

          this.$router.push({ name: 'register-bo-thank-you' })
        }

      } catch (e) {
        console.log(`error`, e)
        this.isDisabled = false
        this.showDialogNotification(`error`, this.$t('business.try_again'))
      }
    },
    async uploadProduct(payload) {
      try {
        await RunnerService.createProduct(this.getStep0.id, payload)
      } catch (e) {
        console.log(`e`, e)
        this.showDialogNotification(`error`, `Something went wrong`)
      }
    },
    ...mapActions([
      '_setBizDetails_',
      'clearSteps'
    ])
  },
  components: {
    homeMenu: () => import('@/components/home-menu')
  },
  computed: {
    ...mapGetters({
      user: 'currentUser',
      getStep0: 'getStep0',
      getStep1: 'getStep1',
      getStep2: 'getStep2',
      getStep3: 'getStep3',
      getStep3Identity: 'getStep3Identity',
      getStep4: 'getStep4'
    })
  },
  mounted () {
    this._initializeNotchTemplate('#fff', 'default')
    this.validateBusinessFields()
  }
}
</script>
