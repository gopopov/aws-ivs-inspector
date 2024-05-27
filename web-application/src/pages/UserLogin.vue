<template>
  <div class="column q-gutter-y-md flex flex-center text-center q-pt-md">
    <div style="padding: var(--amplify-space-small); text-align: center">
      <q-img width="100px" alt="Amplify logo" src="/icons/ivs.png" />
    </div>

    <div class="auth-card">
      <q-form
        greedy
        ref="loginForm"
        class="q-gutter-y-md"
        @submit.prevent="submitForm"
      >
        <div
          class="q-col-gutter-y-md"
          :style="
            $q.screen.lt.sm
              ? 'width: calc(100vw - 90px);max-width: calc(100vw - 90px)'
              : 'width: 400px'
          "
        >
          <q-input
            bottom-slots
            label="Email"
            v-model="formData.email"
            lazy-rules
            :rules="[
              (val) =>
                commonStore.isValidEmailAddress(val) ||
                'Provide valid Email ID',
            ]"
            ref="email"
            type="email"
          >
            <template v-slot:before>
              <q-icon name="account_circle" />
            </template>

            <template v-slot:append>
              <q-icon
                v-if="formData.email !== ''"
                name="close"
                @click="formData.email = ''"
                class="cursor-pointer"
              />
            </template>
          </q-input>

          <q-input
            bottom-slots
            label="Password"
            v-model="formData.password"
            lazy-rules
            :rules="[
              (val) =>
                (val && val.length >= 6) || 'Password length is insufficient',
            ]"
            type="password"
            ref="password"
          >
            <template v-slot:before>
              <q-icon name="password" />
            </template>

            <template v-slot:append>
              <q-icon
                v-if="formData.password !== ''"
                name="close"
                @click="formData.password = ''"
                class="cursor-pointer"
              />
            </template>
          </q-input>
        </div>

        <div class="row justify-between">
          <div class="col-auto text-grey self-center">
            <q-item
              class="q-px-xs text-body1"
              clickable
              @click="passwordReset = !passwordReset"
            >
              <q-item-section avatar v-if="passwordReset">
                <q-icon class="border" name="arrow_back_ios" />
              </q-item-section>
              <q-item-section>
                {{ passwordReset ? "Login" : "Forgot password?" }}
              </q-item-section>
            </q-item>
          </div>
          <div class="col-auto self-center">
            <q-btn
              v-if="!passwordReset"
              outline
              rounded
              dense
              no-caps
              :loading="loading"
              class="q-px-md q-py-xs text-body1"
              label="Log In"
              type="submit"
            />
            <q-btn
              v-else
              outline
              rounded
              dense
              no-caps
              class="q-px-md q-py-xs text-body1"
              label="Reset"
              @click="resetPassword"
            />
          </div>
        </div>
      </q-form>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, computed, onMounted } from "vue";
import { useQuasar } from "quasar";
import { useRoute, useRouter } from "vue-router";
import { useCommonStore } from "src/stores/store-common";
import { useAuthStore } from "src/stores/store-auth";

export default defineComponent({
  name: "UserLogin",

  setup(_, { emit }) {
    const $q = useQuasar();
    const $route = useRoute();
    const $router = useRouter();
    const authStore = useAuthStore();
    const commonStore = useCommonStore();

    const loading = ref(false);
    const passwordReset = ref(false);
    const isPwd = ref(true);
    const formData = ref({
      email: "sathia.s@hotmail.com",
      password: "Sath!a007",
    });
    const loginForm = ref();

    const submitForm = () => {
      loading.value = true;
      authStore.userSignIn(formData.value).then((response) => {
        console.log(response);
        if (response.code == "auth/user-not-found") {
          $q.notify({
            color: "red",
            textColor: "white",
            position: "top-right",
            icon: "thumb_down",
            timeout: 1500,
            message: "Invalid Email Address",
            actions: [
              {
                icon: "close",
                color: "white",
                handler: () => {},
              },
            ],
          });
          loading.value = false;
        } else if (response.code == "auth/wrong-password") {
          $q.notify({
            color: "red",
            textColor: "white",
            position: "top-right",
            icon: "thumb_down",
            timeout: 1500,
            message: "Invalid Password",
            actions: [
              {
                icon: "close",
                color: "white",
                handler: () => {},
              },
            ],
          });
          loading.value = false;
        } else if (response.code == "login success") {
          loading.value = false;
          $router.push($route.query.redirect || "/").catch((err) => {});
        } else if (response.code == "user unauthorised") {
          $q.notify({
            color: "red",
            textColor: "white",
            position: "top-right",
            icon: "thumb_down",
            timeout: 1500,
            message: "User Unauthorised",
            actions: [
              {
                icon: "close",
                color: "white",
                handler: () => {},
              },
            ],
          });
          loading.value = false;
        }
      });
    };

    const resetPassword = () => {
      authStore.resetUserPassword(formData.value.email).then((response) => {
        console.log(response);
        if (response.code == "check mail") {
          passwordReset.value = false;
          loginForm.value.reset();
          $q.notify({
            color: "green",
            textColor: "white",
            position: "top-right",
            icon: "",
            timeout: 1500,
            message:
              "Password reset link sent, please check your mail inbox/junk folder",
            actions: [
              {
                icon: "close",
                color: "white",
                handler: () => {},
              },
            ],
          });
        } else if (response.code == "auth/wrong-password") {
          $q.notify({
            color: "red",
            textColor: "white",
            position: "top-right",
            icon: "thumb_down",
            timeout: 1500,
            message: "Invalid Password",
            actions: [
              {
                icon: "close",
                color: "white",
                handler: () => {},
              },
            ],
          });
        }
      });
    };

    const resetForm = () => {
      formData.value = {
        email: null,
        password: null,
      };
    };

    onMounted(() => {});

    return {
      commonStore,
      passwordReset,
      isPwd,
      formData,
      loading,

      submitForm,
      resetForm,
      resetPassword,
    };
  },
});
</script>
