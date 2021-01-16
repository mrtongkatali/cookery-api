<template lang="pug">
div
  div
    div#regMenu
      home-menu(:backEnabled="false", themeColor="white", :enableListLink="true")
    div.body-holder.pt-2
      div.mx-3.pt-2
        b-form#flyerForm(data-vv-scope="flyerForm", autocomplete="off")
          b-form-group(:label="`${$t('flyer.registration_key')} *`", class="muted-placeholder")
            b-form-input(type="text", v-model="form.registrationKey", :placeholder="$t('flyer.registration_key')", name="registrationKey", v-validate.lazy="'required'", maxlength="8", class="input-line input-gray")
            small.error.text-danger(v-if="errors.has('registrationKey', 'flyerForm')") {{ errors.first('registrationKey', 'flyerForm') }}

          b-form-group(:label="$t('flyer.flyer_number')", class="muted-placeholder")
            b-form-input(type="tel", v-model="form.flyerNumber", :placeholder="$t('flyer.flyer_number')", name="flyerNumber", maxlength="6", class="input-line input-gray")
            //- small.error.text-danger(v-if="errors.has('flyerNumber', 'flyerForm')") {{ errors.first('flyerNumber', 'flyerForm') }}

          //- b-form-group(:label="$t('flyer.lucky_draw_option')", class="muted-placeholder")
            multiselect(
              v-model="luckyDrawOption.selected",
              track-by="code",
              label="text",
              :options="luckyDrawOption.list",
              name="luckyDrawOption",
              v-validate.lazy="'required'"
            )

            small.error.text-danger(v-if="errors.has('luckyDrawOption', 'flyerForm')") {{ errors.first('luckyDrawOption', 'flyerForm') }}

      div.mx-3.mt-3
        b-button.btn-shadow.w-100(variant="primary", size="md", @click.stop="formSubmit", :disabled="finalizing")
          span {{ $t('business.next') }}
      br.clear
</template>
<script>
import { mapGetters, mapActions } from 'vuex'
import { MiscService, RunnerService } from '@/api'
import Multiselect from 'vue-multiselect'
import 'vue-multiselect/dist/vue-multiselect.min.css'
import { Validator } from 'vee-validate'

const dictionary = {
  custom: {
    registrationKey: {
      required: 'Registration key is a required field'
    },
    flyerNumber: {
      required: 'Flyer number is a required field'
    },
    luckyDrawOption: {
      required: 'Lucky draw option is a required field'
    }
  }
}

Validator.localize('en', dictionary)

export default {
  name: 'flyer-confirmation',
  data () {
    return {
      map: require(`@/assets/static/registration/map.png`),
      uploaderFiller: require(`@/assets/static/registration/profile.png`),
      productBanner: require(`@/assets/static/registration/product.png`),
      picDialog: {
        show: false,
        url: null
      },
      form: {
        registrationKey: null,
        flyerNumber: null
      },
      luckyDrawOption: {
        selected: null,
        list: []
      },
      finalizing: false
    }
  },
  methods: {
    async init () {
      const key = await MiscService.getKey('lucky_draw_option')
      this.luckyDrawOption.list = (key && key.value ? JSON.parse(key.value) : [])
      console.log('this._bizDetails_', this._bizDetails_)
      if (this._bizDetails_ && this._bizDetails_.regKey) {
        this.form.registrationKey = this._bizDetails_.regKey
      }
    },
    async formSubmit () {
      const isValid = await this.$validator.validateAll('flyerForm')
      if (isValid) {
        try {
          this.finalizing = true

          await RunnerService.finalizeFlyerRegistration({
            regKey: this.form.registrationKey,
            flyerNo: this.form.flyerNumber,
            // luckyDraw: this.luckyDrawOption.selected.code
            luckyDraw: null
            // makeLive: this._bizDetails_.currentStatus === 'REGISTERED' ? true : null
          })
          if (this._bizDetails_ && (this._bizDetails_.isBizComplete || this._bizDetails_.currentStatus === 'REGISTERED')) {
            await RunnerService.goLive(this._bizDetails_.id)
            this.addNotification('success filled', this.$t('business.congrats'), this.$t('flyer.new_biz_registration'))
          } else {
            this.addNotification('success filled', this.$t('business.congrats'), this.$t('flyer.biz_draft'))
          }
          // let msg = (this._bizDetails_ && this._bizDetails_.isBizComplete ?  : this.$t('flyer.biz_draft'))
          this.finalizing = false
          // this.addNotification('success filled', this.$t('business.congrats'), this.$t('flyer.new_biz_registration'))

          this.clearSteps()
          this.clearProfile()
          this.$router.push({ name: 'register-bo-thank-you' })
        } catch (e) {
          console.log(`eee`, e)
          this.finalizing = false
          this.showDialogNotification(`error`, this._parseErrorRes(e) || this.$t('adhoc.something_went_wrong'))
        }
      }
    },

    ...mapActions([
      'clearSteps',
      'setDisableBack',
      'setEnableBack',
      'clearProfile'
    ])
  },
  components: {
    Multiselect,
    homeMenu: () => import('@/components/home-menu')
  },
  computed: {
    ...mapGetters({
      _bizDetails_: '_getBizDetails_',
      getStep1: 'getStep1',
      getStep2: 'getStep2',
      getStep3: 'getStep3',
      getStep4: 'getStep4'
    })
  },
  mounted () {
    this.init()
    this.setDisableBack()
  },
  beforeDestroy () {
    this.setEnableBack()
  }
}
</script>
