<template>
  <div class="col q-gutter-sm body-spacing">
    <div class="col">
      <!-- {{ metrics?.[0] }} -->
      <div class="row q-gutter-sm col-12 col-md">
        <div
          v-for="(metric, index) in metrics"
          :key="index"
          class="column col box-decorator"
        >
          <div class="col-auto q-pa-md text-h6">
            <q-item-label class="text-body1">
              {{ metric.Label }}
            </q-item-label>
            <q-item-label caption class="text-primary">
              {{ metric.Datapoints[0]?.Unit }} - 24hrs
            </q-item-label>
          </div>

          <div class="col q-py-lg text-center">
            <q-item-label class="value-text">
              {{
                metric.Datapoints.reduce(
                  (accumulator, current) =>
                    accumulator + current.Sum || current.Maximum,
                  0
                )
              }}
            </q-item-label>
          </div>
        </div>
      </div>
    </div>

    <!-- {{ concurrentStreams }}
    {{ accountStore.metrics?.[ivsRegion]?.[1]["Datapoints"] }} -->
    <div class="col" v-if="metrics">
      <div class="row q-gutter-sm col-12 col-md">
        <q-list class="col box-decorator">
          <q-item dense class="q-pa-md text-h6">
            <q-item-section>
              <q-item-label class="text-body1">
                Concurrent Streams
              </q-item-label>
            </q-item-section>

            <q-item-section side>
              <q-item-label class="text-body1 text-primary">
                24hrs
              </q-item-label>
            </q-item-section>
          </q-item>

          <chart-usage-metrics
            :metrics="accountStore.metrics?.[ivsRegion]?.[1]['Datapoints']"
            label="Concurrent Streams"
          />
        </q-list>

        <q-list class="col box-decorator">
          <q-item dense class="q-pa-md text-h6">
            <q-item-section>
              <q-item-label class="text-body1"> Concurrent Views </q-item-label>
            </q-item-section>

            <q-item-section side>
              <q-item-label class="text-body1 text-primary">
                24hrs
              </q-item-label>
            </q-item-section>
          </q-item>

          <chart-usage-metrics
            :metrics="accountStore.metrics?.[ivsRegion]?.[0]['Datapoints']"
            label="Concurrent Views"
          />
        </q-list>
      </div>
    </div>

    <div class="col">
      <div class="row q-gutter-sm col-12 col-md">
        <div
          v-if="quotasLowLatency?.length"
          class="col q-gutter-y-sm box-decorator"
        >
          <div class="col-auto q-pa-md text-h6">
            <q-item-label class="text-body1">
              Quotas: Low Latency
            </q-item-label>
          </div>

          <q-table
            class="bg-transparent"
            flat
            :rows="quotasLowLatency"
            :columns="columns"
            row-key="QuotaName"
            hide-header
            hide-bottom
          />
        </div>

        <div
          v-if="quotasStages?.length"
          class="col q-gutter-y-sm box-decorator"
        >
          <div class="col-auto q-pa-md text-h6">
            <q-item-label class="text-body1"> Quotas: Stages </q-item-label>
          </div>

          <q-table
            class="bg-transparent"
            flat
            :rows="quotasStages"
            :columns="columns"
            row-key="QuotaName"
            hide-header
            hide-bottom
            :pagination="initialPagination"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, defineComponent, onMounted, ref } from "vue";
import { useAccountStore } from "src/stores/store-account";
import { useCommonStore } from "src/stores/store-common";
import { useRoute } from "vue-router";
import ChartUsageMetrics from "src/components/Charts/ChartUsageMetrics.vue";

export default defineComponent({
  name: "DashBoard",

  setup() {
    const commonStore = useCommonStore();
    const accountStore = useAccountStore();
    const $route = useRoute();
    const ivsRegion = $route.params.region;

    const concurrentViews = computed(
      () => accountStore.metrics?.[ivsRegion]?.[0]["Datapoints"]
    );

    const concurrentStreams = computed(
      () => accountStore.metrics?.[ivsRegion]?.[1]["Datapoints"]
    );

    const metrics = computed(() => {
      var metricsManipulation = accountStore.metrics[ivsRegion];
      console.log(metricsManipulation);
      // const ConcurrentViews = metricsManipulation?.[0]?.["Datapoints"].sort(
      //   (x, y) =>
      //     new Date(y.Timestamp).getTime() - new Date(x.Timestamp).getTime()
      // )?.[0];
      // const ConcurrentStreams = metricsManipulation?.[1]?.["Datapoints"].sort(
      //   (x, y) =>
      //     new Date(y.Timestamp).getTime() - new Date(x.Timestamp).getTime()
      // )?.[0];

      // console.log("", ConcurrentStreams);
      // if (metricsManipulation) {
      //   metricsManipulation[0]["Datapoints"] = [ConcurrentViews];
      //   metricsManipulation[1]["Datapoints"] = [ConcurrentStreams];
      // }
      return metricsManipulation;
    });

    const quotasProvisioned = computed(
      () => accountStore.accountQuotas[ivsRegion]
    );

    const quotasLowLatencyKeys = [
      "Channels",
      "Concurrent streams",
      "Concurrent views",
      "Playback restriction policies",
      "Recording configurations",
    ];

    const quotasStagesKeys = [
      "Stages",
      "Stream Key",
      "Total number of Destinations per Composition",
      "Compositions",
      "Stage participants (subscribers)",
      "Stage participants (publishers)",
      "Max Composition duration",
      "Storage configurations",
      "Encoder configurations",
    ];

    const quotasLowLatency = computed(() =>
      quotasProvisioned?.value?.filter((quota) =>
        quotasLowLatencyKeys.includes(quota.QuotaName)
      )
    );

    const quotasStages = computed(() =>
      quotasProvisioned?.value?.filter((quota) =>
        quotasStagesKeys.includes(quota.QuotaName)
      )
    );

    const columns = [
      {
        name: "QuotaName",
        required: true,
        label: "Quota Name",
        align: "left",
        field: (row) => row.QuotaName,
        format: (val) => `${val}`,
        sortable: true,
      },
      {
        name: "Value",
        required: true,
        label: "Provisioned",
        align: "right",
        field: (row) => row.Value,
        format: (val) => `${val}`,
        sortable: true,
      },
    ];

    onMounted(() => {
      if (!quotasProvisioned.value?.length) {
        accountStore.getQuotaProvisioned("ivs", ivsRegion);
      }

      accountStore.getMetrics(ivsRegion);
    });

    return {
      metrics,
      concurrentViews,
      concurrentStreams,
      quotasProvisioned,
      accountStore,
      quotasLowLatency,
      quotasStages,
      columns,
      ivsRegion,
      initialPagination: commonStore.initialPagination,
    };
  },

  // eslint-disable-next-line vue/no-unused-components
  components: { ChartUsageMetrics },
});
</script>

<style lang="sass">
.box-decorator
  background-color: $grey-2
  border: 1px solid #ff9900

.value-text
  font-size: 4vw
  font-weight: 400
  color: $grey-8
</style>
