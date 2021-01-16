<template lang="pug">
div
  div#regMenu
    home-menu(:backEnabled="false", themeColor="white", :enableListLink="true", :myRoute="{ name: 'business-users-list' }")
  div.body-holder.pt-2.success-container
    div.mx-3.text-center.center-vertical
      img(:src="emailImg", width="180px")
      div.content-email.pt-2
        h4.font-weight-bold {{ $t('business.register_biz_thanks') }}
        span {{ $t('business.we_register_biz') }} #[br] {{ $t('business.receive_sms') }}
      div.mb-2.mt-3
        b-button.btn-shadow.w-100(variant="info", size="md", @click="registerLink")
          span {{ $t('business.register_new_biz') }}
      div
        b-button.btn-shadow.w-100(variant="primary", size="md", @click="listLink")
          span {{ $t('business.view_all_biz') }}
</template>
<script>
import { mapActions } from 'vuex'
export default {
  name: 'register-bo-thank-you',
  data () {
    return {
      emailImg: require(`@/assets/static/registration/email.png`)
    }
  },
  components: {
    homeMenu: () => import('@/components/home-menu')
  },
  mounted () {
    this._initializeNotchTemplate('#fff', 'default')
    this.clearSteps()
  },
  created () {
  },
  methods: {
    ...mapActions([
      'clearSteps'
    ]),
    registerLink () {
      this.$router.push({ name: 'register-business-owner' })
    },
    listLink () {
      this.$router.push({ name: 'business-users-list' })
    }
  }
}
</script>
