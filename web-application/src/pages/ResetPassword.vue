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
      ref="resetUserPasswordCode"
      @submit.prevent="resetUserPasswordCode"
      @reset="resetData"
      class="q-gutter-y-md q-px-md bg-dark-8 q-pb-md"
      :style="$q.screen.width > 350 ? `min-width: 350px` : `min-width: 100vw`"
    >
      <q-input
        class="col"
        dark
        type="email"
        v-model="email"
        label="Email Address"
      />
      <q-input
        class="col"
        dark
        type="password"
        v-model="newPassword"
        label="New Password"
      />
      <q-input class="col" dark type="password" v-model="code" label="Code" />
      <q-btn unelevated stretch type="submit" color="blue-grey">
        Reset Password
      </q-btn>
    </q-form>

    <!-- <span class="flex text-h5 text-dark-3">Reset User Code</span>
    <q-form
      ref="resendConfirmSignUp"
      @submit.prevent="resendConfirmationCode"
      @reset="resetData"
      class="q-gutter-y-md q-px-md bg-dark-8 q-pb-md"
      :style="$q.screen.width > 350 ? `min-width: 350px` : `min-width: 100vw`"
    >
      <q-input
        class="col"
        dark
        type="email"
        v-model="email"
        label="Email Address"
      />
      <q-btn unelevated type="submit" color="blue-grey">
        Resend Confirm Code
      </q-btn>
    </q-form> -->
  </div>
</template>

<script>
import { Auth } from "aws-amplify";

export default {
  data() {
    return {
      email: "",
      newPassword: "",
      code: "",
      loading: false
    };
  },

  methods: {
    resetUserPasswordCode() {
      Auth.forgotPasswordSubmit(this.email, this.code, this.newPassword)
        .then(() => {
          this.$q.notify({
            classes: "border bg-dark-8",
            textColor: "white",
            position: "top-right",
            icon: "task_alt",
            timeout: 1500,
            message: "Your password successfully reset now!"
          });

          this.$router.push("/login");
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
          this.$refs.resetUserPasswordCode.reset();
        });
    },

    resendConfirmationCode() {
      Auth.resendSignUp(this.email)
        .then(res => {
          console.log(res);
          this.$q.notify({
            classes: "border bg-dark-8",
            textColor: "white",
            position: "top-right",
            icon: "task_alt",
            timeout: 1500,
            message: "New confirmation code resent successfully"
          });
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
          this.$refs.resendConfirmSignUp.reset();
        });
    },

    resetData() {
      this.email = "";
      this.newPassword = "";
    }
  }
};
</script>
