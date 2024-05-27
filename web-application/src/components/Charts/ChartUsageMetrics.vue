<template>
  <v-chart
    v-if="option?.series?.data.length"
    class="ivs-bg-grey q-pa-md"
    :option="option"
    autoresize
  />
</template>

<script>
import { defineComponent, onMounted, ref, provide, computed } from "vue";

import { date } from "quasar";
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { BarChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  ToolboxComponent,
  DataZoomComponent,
} from "echarts/components";

import VChart, { THEME_KEY } from "vue-echarts";

use([
  CanvasRenderer,
  BarChart,
  GridComponent,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  ToolboxComponent,
  DataZoomComponent,
]);

export default defineComponent({
  name: "UsageMetricsChart",

  props: {
    label: { type: String, default: null },
    metrics: { type: Array, default: null },
  },

  components: { VChart },

  setup(props) {
    provide(THEME_KEY);

    const option = ref({
      tooltip: {
        trigger: "axis",
        axisPointer: {
          type: "shadow",
        },
      },

      grid: {
        left: "3%",
        right: "3%",
        top: "10%",
        bottom: "25%",
        containLabel: true,
      },

      dataZoom: [
        {
          show: true,
          realtime: true,
          start: 0,
          end: 100,
          xAxisIndex: [0, 1],
        },
        {
          type: "inside",
          realtime: true,
          start: 30,
          end: 70,
          xAxisIndex: [0, 1],
        },
      ],

      toolbox: {
        // feature: {
        //   saveAsImage: {},
        // },
      },

      xAxis: {
        type: "category",
        boundaryGap: true,
        data: [],
      },

      yAxis: {
        min: null,
        max: null,
      },

      series: {
        name: props.label,
        type: "bar",
        stack: "Total",
        data: [],
      },
    });

    const metrics = props.metrics;

    const manipulateMetrics = () => {
      option.value.xAxis.data = metrics
        ?.sort(
          (x, y) =>
            new Date(x.Timestamp).getTime() - new Date(y.Timestamp).getTime()
        )
        .map((data) => date.formatDate(data.Timestamp, "hh:mm:ss"));

      option.value.series.data = metrics?.map((data) => data.Sum);
      option.value.yAxis.min = Math.min(...option.value.series.data);
      option.value.yAxis.max = Math.max(...option.value.series.data);
    };

    onMounted(() => {
      manipulateMetrics();
    });

    return { option };
  },
});
</script>

<style scoped>
.echarts {
  width: 100%;
  height: 200px;
  margin: auto auto;
}
.echart {
  width: 100%;
  height: 200px;
  /* border: 1px solid #cfcfcf; */
}
h1,
h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 10px;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
