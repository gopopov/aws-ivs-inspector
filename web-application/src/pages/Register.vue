<template>
  <div class="column q-gutter-y-md flex flex-center text-center q-pt-md">
    <span class="col text-h5 text-dark-3">Register User</span>
    <q-form
      ref="registration"
      @submit.prevent="register"
      @reset="resetData"
      class="q-gutter-y-md q-px-md bg-dark-8 q-pb-md"
      :style="$q.screen.width > 350 ? `min-width: 350px` : `min-width: 100vw`"
    >
      <q-input
        class="col"
        dark
        v-model="organisation_id"
        label="Organisation ID"
      />
      <q-input
        class="col"
        dark
        v-model="organisation_name"
        label="Organisation Name"
      />
      <q-input class="col" dark v-model="email" label="User Name" />
      <q-input
        class="col"
        dark
        type="password"
        v-model="password"
        label="Password"
      />
      <q-btn unelevated type="submit" color="blue-grey">Register</q-btn>
    </q-form>

    <span class="col text-h5 text-dark-3">Confirm User</span>
    <q-form
      ref="confirmSignUp"
      @submit.prevent="confirmationCode"
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
      <q-input class="col" dark type="password" v-model="code" label="Code" />
      <q-btn unelevated type="submit" color="blue-grey">Confirm User</q-btn>
    </q-form>
  </div>
</template>

<script>
import { Auth } from "aws-amplify";

export default {
  data() {
    return {
      organisation_id: "",
      organisation_name: "",
      email: "",
      password: "",
      newPassword: "",
      code: "",
      loading: false
    };
  },

  methods: {
    register() {
      // console.log("registering");
      Auth.signUp({
        username: this.email,
        password: this.password,
        attributes: {
          "custom:organisation_id": this.organisation_id.replace(/ /g, ""),
          "custom:organisation_name": this.organisation_name
        }
      })
        .then(res => {
          this.$q.notify({
            classes: "border bg-dark-8",
            textColor: "white",
            position: "top-right",
            icon: "warning",
            timeout: 1500,
            message: "User successfully registered. Please login"
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
          this.$refs.registration.reset();
        });
    },

    confirmationCode() {
      Auth.confirmSignUp(this.email, this.code)
        .then(res => {
          console.log(res);
          this.$q.notify({
            classes: "border bg-dark-8",
            textColor: "white",
            position: "top-right",
            icon: "task_alt",
            timeout: 1500,
            message: "Thank you for the confirmation"
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
          this.$refs.confirmSignUp.reset();
        });
    },

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
          this.$refs.forgotPassword.reset();
        });
    },

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
      this.password = "";
    }
  }
};
</script>
