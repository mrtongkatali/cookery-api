<template lang="pug">
div
  div.overlay-preview.preview-img(v-if="picDialog.show && picDialog.url")
    i.simple-icon-close.preview-close(@click="closePreview")
    img(:src="_fullUrlRef(picDialog.url, 480)")
  div
    div#regMenu
      home-menu(:backEnabled="true", themeColor="white", :enableListLink="true")
    div.body-holder.pt-2
      div.mx-3.mt-2(v-if="product && product.length === 0", :class="product.length === 0 ? 'product-vertical' : ''")
        h4.font-weight-normal.mx-auto.text-center {{ $t('business.add_products') }}
        img.product-banner(:src="productBanner")
      div.mx-3(v-for="(product, idx) in product", :key="idx")
        image-uploader(:showDialogBox="product.showDialogBox", :label="$t('business.how_photo')" @onDialogClose="onDialogClose", @onProductImageUploaded="onProductImageUpload", :productKey="idx", @onImageUploading="onImageUploading")
        div.product-title-container
          //- span.title-page.w-60(@click="sampleImg(idx)") Business Product {{ idx + 1 }}
          span.title-page.w-60.left {{ $t('business.business_product') }} {{ idx + 1 }}
          i.simple-icon-close.remove-product-icon(@click="removeProduct(idx)")
        b-form#BoStep4(data-vv-scope="BoStep4", autocomplete="off")
          div
            b-form-group(:label="$t('business.product_name')", class="muted-placeholder")
              b-form-input(type="text", v-model="product.title", :placeholder="$t('business.enter_product_name')", name="productName", maxlength="50", class="left input-line input-gray")
              small.error.text-danger(v-if="hasError(idx, 'title')") {{ getError(idx, 'title') }}

            b-form-group(:label="$t('business.category')", class="muted-placeholder")
              multiselect(
                v-model="product.category",
                :placeholder="$t('business.select_category')",
                :show-labels="false",
                :options="categories",
                name="category"
              )
                span(slot="noResult") {{ $t('mobileInput.invalid') }}
              small.error.text-danger(v-if="hasError(idx, 'category')") {{ getError(idx, 'category') }}

            b-form-group(:label="$t('business.description')", class="muted-placeholder")
              b-form-input(type="text", v-model="product.description", :placeholder="$t('business.enter_description')", name="description", v-validate.lazy="'required'", maxlength="50", class="left input-line input-gray")
              small.error.text-danger(v-if="hasError(idx, 'description')") {{ getError(idx, 'description') }}

            b-form-group(:label="$t('business.price')", class="muted-placeholder")
              b-form-input(type="text", v-model="currency", :disabled="true", :placeholder="$t('business.currency')", name="currency", maxlength="1", class="input-line input-gray currency-input")
              b-form-input(type="number", v-model="product.price", :placeholder="$t('business.enter_price')", name="price", v-validate.lazy="'required'", maxlength="50", class="input-line input-gray price-input")
              small.error.text-danger(v-if="hasError(idx, 'price')") {{ getError(idx, 'price') }}

            b-form-group(:label="$t('business.sizes')", class="muted-placeholder")
              //- b-form-group
                b-form-radio-group(id="btn-radios-1", v-model="product.productSize", :options="sizeOption", buttons, button-variant="outline-primary", name="radios-btn-default")
              multiselect(
                v-model="product.productSize",
                :placeholder="$t('business.select_size')",
                :show-labels="false",
                :options="sizeOption",
                name="val"
              )
                span(slot="noResult") {{ $t('mobileInput.invalid') }}
              small.error.text-danger(v-if="hasError(idx, 'productSize')") {{ getError(idx, 'productSize') }}
              //- b-form-input(type="number", v-model="product.weightInGrams", placeholder="Enter product weight", name="weight", v-validate.lazy="'required'", maxlength="50", class="input-line input-gray")
              //- small.error.text-danger(v-if="hasError(idx, 'weightInGrams')") {{ getError(idx, 'weightInGrams') }}

            b-alert(show, variant="danger", v-if="hasError(idx, 'images')") {{ getError(idx, 'images') }}
            b-form-group(:label="$t('business.upload_best_photo')", class="muted-placeholder margin-t-27")
              div.upload-filler-container(@click="openProductDialog(idx)")
                div.left.filler-box.product-photo
                  i.iconsminds-add-file.vertical-icon
              div.product-photo(v-if="product.images && product.images.length > 0", v-for="(i, ctr) in product.images", :key="ctr")
                i.simple-icon-close.remove-photo(@click="removeProductPhoto(idx, ctr)")
                div.uploaded-product(:style="{ backgroundImage : 'url(' + i + ')' }", @click="showPicDialog(i)")
      div.mx-3.mb-1.mt-1
        b-button.btn-shadow.w-100.blue-btn.pr-1.pl-1.mr-1.colr-5(variant="info", size="md", @click="addNewProduct", :disabled="isDisabled || hasPendingUploads")
          span(v-if="product && product.length === 0") {{ $t('business.add_product') }}
          span(v-else) {{ $t('business.add_another_product') }}
        b-button.btn-shadow.w-100.pr-1.pl-1.colr-5(variant="primary", size="md", @click="formSubmit", :disabled="isDisabled || hasPendingUploads")
          span {{ $t('business.submit') }}
      br.clear
</template>
<script>
import { mapGetters, mapActions } from 'vuex'
import { MiscService } from '@/api'
import { map, each } from 'lodash/collection'
import { Validator } from 'vee-validate'
import { isEmpty } from 'lodash/lang'
import Multiselect from 'vue-multiselect'
import 'vue-multiselect/dist/vue-multiselect.min.css'
const dictionary = {
  custom: {
    ageGroup: {
      required: 'Age Group is required.'
    }
  }
}

Validator.localize('en', dictionary)
export default {
  name: 'business-register-step4',
  data () {
    return {
      map: require(`@/assets/static/registration/map.png`),
      uploaderFiller: require(`@/assets/static/registration/profile.png`),
      productBanner: require(`@/assets/static/registration/product.png`),
      // categories: ['Fashion', 'Tech', 'Others'],
      categories: [],
      currency: '₹',
      isDisabled: false,
      product: [],
      position: null,
      picDialog: {
        show: false,
        url: null
      },
      productErrors: [],
      sizeOption: ['Small', 'Medium', 'Large'],
      isDirty: false,
      imgUploadingCount: 0
    }
  },
  components: {
    homeMenu: () => import('@/components/home-menu'),
    imageUploader: () => import('@/components/Widgets/ImageUploader'),
    Multiselect
  },
  mounted () {
    this._initializeNotchTemplate('#fff', 'default')
    this.init()
    if (this.getStep4) {
      this.product = this.getStep4
    }
  },
  watch: {
    product: {
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
      getStep1: 'getStep1',
      getStep2: 'getStep2',
      getStep3: 'getStep3',
      getStep4: 'getStep4'
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
          this.setStep4(this.product)
          this.isDirty = false
        }, 5000)
      }
    },
    setDirtyForm () {
      this.isDirty = true
    },
    ...mapActions([
      'setStep4'
    ]),
    async init () {
      let response = await MiscService.getKey('category')
      this.categories = map(JSON.parse(response.value), 'title')
    },
    sampleImg (key) {
      let product = this.product[key]
      product.images.push(`https://images.pexels.com/photos/767239/pexels-photo-767239.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260`)
    },
    openProductDialog (key) {
      let product = this.product[key]
      product.showDialogBox = true
    },
    onDialogClose (key) {
      let product = this.product[key]
      product.showDialogBox = false
    },
    onProductImageUpload (fsRef, key) {
      let product = this.product[key]
      product.images.push(this.assetsURL(fsRef))
    },
    setCategory (cat, product) {
      product.category = cat
    },
    onScroll (e, position) {
      this.position = position
      if (this.position.scrollTop > 25) {
        document.getElementById('regMenu').classList.add('nav-scroll-border')
      } else {
        document.getElementById('regMenu').classList.remove('nav-scroll-border')
      }
    },
    addNewProduct () {
      let payload = {
        title: null,
        category: null,
        description: null,
        price: 0,
        images: [],
        weightInGrams: 0,
        showDialogBox: false
      }
      this.product.push(payload)
    },
    validateProduct () {
      this.productErrors = {}
      if (this.product && this.product.length > 0) {
        each(this.product, (prod, idx) => {
          if (!prod.title) this.setError(idx, 'title', `Product name is required`)
          if (!prod.category) this.setError(idx, 'category', `Category is required`)
          if (!prod.description) this.setError(idx, 'description', `Description is required`)
          // if (prod.images && prod.images.length === 0) this.setError(idx, 'images', `1 or more image must be uploaded`)
        })
      }
      return isEmpty(this.productErrors)
    },
    setError (idx, field, message) {
      if (this.productErrors.hasOwnProperty(idx)) {
        this.productErrors[idx][field] = message
      } else {
        this.$set(this.productErrors, idx, {})
        this.$set(this.productErrors[idx], field, message)
      }
    },
    hasError (idx, field) {
      if (this.productErrors.hasOwnProperty(idx)) {
        return this.productErrors[idx].hasOwnProperty(field)
      } else {
        return false
      }
    },
    getError (idx, field) {
      return this.productErrors[idx][field]
    },
    async formSubmit () {
      let isValidProduct = this.validateProduct()
      if (isValidProduct) {
        this.setStep4(this.product)
        this.$router.push({ name: 'registration-summary' })
      }
    },
    removeProduct (idx) {
      this.product.splice(idx, 1)
    },
    removeProductPhoto (productIndex, photoIndex) {
      let product = this.product[productIndex]
      product.images.splice(photoIndex, 1)
      this.addNotification('warning filled', this.$t('business.product_removed'), ``)
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
