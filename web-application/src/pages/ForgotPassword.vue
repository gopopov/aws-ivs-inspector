<template>
  <div class="column q-gutter-y-md flex flex-center text-center q-pt-md">
    <div class="flex text-h4 text-dark-3 q-gutter-x-sm">
      <div v-if="$q.screen.width > 320" class="self-center">
        <span>Deliver</span>
        <span class="text-light-green">Ad</span>
        <span class="text-re"> X</span>
      </div>
    </div>
    <q-form
      ref="forgotPassword"
      @submit.prevent="forgotPassword"
      @reset="resetData"
      class="q-gutter-y-md q-px-md bg-dark-8 q-pb-md"
      :style="$q.screen.width > 350 ? `min-width: 350px` : `min-width: 100vw`"
    >
      <q-input
        class="col"
        dark
        type="email"
        color="light-green"
        v-model="email"
        label="Email Address"
      />
      <q-btn
        unelevated
        stretch
        type="submit"
        color="blue-grey"
        label="Forgot Password"
        no-caps
      />
    </q-form>

    <div
      @click="$router.push('/login')"
      class="col text-caption cursor-pointer text-dark-3"
    >
      login
    </div>
  </div>
</template>

<script>
import { Auth } from "aws-amplify";

export default {
  data() {
    return {
      email: ""
    };
  },

  methods: {
    forgotPassword() {
      Auth.forgotPassword(this.email)
        .then(res => {
          console.log("Password reset code: ", res);
          this.$q.notify({
            classes: "border bg-dark-8",
            textColor: "white",
            position: "top-right",
            icon: "task_alt",
            timeout: 1500,
            message: `Password reset code sent to your ${res.CodeDeliveryDetails.AttributeName}, please check.`
          });
          this.$router.push("/reset_password");
        })
        .catch(error => {
          this.$q.notify({
            classes: "border bg-dark-8",
            textColor: "white",
            position: "top-right",
            icon: "warning",
            timeout: 1500,
            message: error.message
          });
        });
    },

    resetData() {
      this.email = "";
    }
  }
};
</script>
