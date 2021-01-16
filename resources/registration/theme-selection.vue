<template lang="pug">
div
  div.overlay-preview-theme.preview-img-theme(v-if="picDialog.show && picDialog.url")
    i.simple-icon-close.preview-close-theme(@click="closePreview")
    img(v-lazy=`{src: picDialog.url, error: static.noPhoto, loading: static.loadingXl}`, alt="image", class="image")
    div.mx-3.mt-2
      b-button.btn-shadow.w-100(variant="primary", size="md", @click="selectTemplate(picDialog.idx)")
        span {{ $t('theme_selection.select_template') }}
  div
    div#regMenu
      home-menu(themeColor="white")
    div.body-holder.mb-2
      div.theme-container.pt-2
        h5.text-center.font-weight-normal {{ $t('theme_selection.select_website_template') }}
      div(class="row ml-1 mr-1")
        div(class="col-6 mb-1 pt-1 theme-card", v-for="(loop, idx) in theme.list", :key="idx", :class="loop.code === theme.selected.code ? 'selected' : ''")
          div(class="imageWrapper", @click="showPicDialog(loop.img, idx)")
            img(v-lazy=`{src: loop.img, error: static.noPhoto, loading: static.loading}`, alt="image", class="image")
            span.theme-name.d-block.text-center.mt-05(:class="loop.code === theme.selected.code ? 'text-white' : 'text-dark'") {{ loop.name }}
      div.mx-3.mt-1.mb-4(id="themeBtn")
        b-button.btn-shadow.w-100(variant="primary", size="md", @click="formSubmit")
          span {{ $t('business.continue') }}
      br
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import { Validator } from 'vee-validate'
import { MiscService, RunnerService } from '@/api'
import Multiselect from 'vue-multiselect'
import 'vue-multiselect/dist/vue-multiselect.min.css'
import 'vue2-timepicker/dist/VueTimepicker.css'
const dictionary = {
  custom: {
    themes: {
      required: `Theme is required`
    }
  }
}

Validator.localize('en', dictionary)

export default {
  name: 'theme-selection',
  data () {
    return {
      emailImg: require(`@/assets/static/registration/email.png`),
      position: null,
      selectedIdx: null,
      theme: {
        selected: {
          name: null,
          code: null,
          src: null,
          preview: null
        },
        list: []
      },
      picDialog: {
        show: false,
        url: null,
        idx: null
      },
      static: {
        loading: require(`@/assets/static/loading/loading.gif`),
        loadingXl: require(`@/assets/static/loading/loading-xl.gif`),
        noPhoto: require(`@/assets/static/loading/no-image.jpg`)
      }
    }
  },
  methods: {
    onAfterSlideChange (e) {
      this.theme.selected = this.theme.list[e]
    },
    async formSubmit () {
      let step2 = this.getStep2
      if (!step2) {
        step2 = {
          theme: null
        }
      }
      step2.theme = this.theme.selected
      this.setStep2(step2)
      try {
        let payload = {
          theme: this.getStep2.theme ? this.getStep2.theme.code : null
        }
        console.log('payload', payload)
        await RunnerService.updateBusiness(this.Step0.id, payload)
      } catch (e) {
        console.log(`e`, e)
        this.showDialogNotification(`error`, `Something went wrong`)
      }
      this.$router.push({ name: 'step-3' })
    },
    async loadData () {
      let res = await MiscService.getKey('business_themes')
      this.theme.list = (res && res.value ? JSON.parse(res.value) : [])
      if (this.getStep2) {
        try {
          if (this.getStep2.theme.code) {
            this.theme.selected = this.getStep2.theme
          }
        } catch {
          let step2 = this.getStep2
          if (!step2) {
            step2 = {
              theme: null
            }
          }
          step2.theme = this.theme.selected
          this.setStep2(step2)
        }
      }
    },
    ...mapActions([
      'clearSteps',
      'setStep2'
    ]),
    registerLink () {
      this.$router.push({ name: 'register-business-owner' })
    },
    listLink () {
      this.$router.push({ name: 'business-users-list' })
    },
    showPicDialog (img, idx) {
      this.picDialog.url = img
      this.picDialog.idx = idx
      this.picDialog.show = true
    },
    closePreview () {
      this.picDialog.url = null
      this.picDialog.show = false
    },
    selectTemplate (idx) {
      this.theme.selected = this.theme.list[idx]
      this.selectedIdx = idx
      this.picDialog.show = false
      this.picDialog.url = null
      this.picDialog.idx = null
      setTimeout(() => {
        document.getElementById('themeBtn').scrollIntoView(true)
      }, 400)
    }
  },
  components: {
    Multiselect,
    homeMenu: () => import('@/components/home-menu')
  },
  computed: {
    ...mapGetters({
      getStep2: 'getStep2',
      Step0: 'getStep0'
    })
  },
  mounted () {
    this._initializeNotchTemplate('#fff', 'default')
    this.loadData()
  }
}
</script>
