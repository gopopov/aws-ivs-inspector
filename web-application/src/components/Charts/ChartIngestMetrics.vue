<template>
  <!-- {{ option?.series[1]?.data }} -->
  <!-- {{ Object.values(metrics).map((value) => Math.trunc(value / 1024)) }} -->
  <v-chart
    v-if="option?.series?.data.length"
    class="ivs-bg-grey q-pa-md"
    :option="option"
    autoresize
  />
</template>

<script>
import { defineComponent, onMounted, ref, provide } from "vue";

import { date } from "quasar";
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { PieChart, LineChart } from "echarts/charts";
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
  PieChart,
  LineChart,
  GridComponent,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  ToolboxComponent,
  DataZoomComponent,
]);

export default defineComponent({
  name: "IngestMetricsChart",

  props: {
    label: { type: String, default: null },
    metrics: { type: Object, default: null },
  },

  components: { VChart },

  setup(props) {
    provide(THEME_KEY);

    const option = ref({
      tooltip: {
        trigger: "axis",
      },

      grid: {
        left: "2%",
        right: "2%",
        top: "10%",
        bottom: "15%",
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
        beginAtZero: true,
        type: "value",
        min: null,
        max: null,
        boundaryGap: [0, "100%"],
        // splitLine: {
        //   show: true,
        // },
      },

      series: {
        name: props.label,
        type: "line",
        stack: "Total",
        data: [],

        // markPoint: {
        //   data: [
        //     {
        //       name: "test",
        //       value: "SS",
        //       xAxis: 1,
        //       yAxis: -0.5,
        //     },
        //   ],
        // },
      },
    });

    const manipulateMetrics = () => {
      option.value.xAxis.data = Object.keys(props.metrics).map((key) =>
        date.formatDate(parseInt(key) * 1000, "hh:mm:ss")
      );

      if (props.label == "Ingest Video Bitrate (kbps)") {
        option.value.series.data = Object.values(props.metrics).map((value) =>
          Math.trunc(value / 1024)
        );
        option.value.yAxis.min = Math.min(...option.value.series.data);
        option.value.yAxis.max = Math.max(...option.value.series.data);
      }
      if (props.label == "Ingest Audio Bitrate (kbps)") {
        option.value.series.data = Object.values(props.metrics).map((value) =>
          Math.trunc(value / 1024)
        );
        option.value.yAxis.min = Math.min(...option.value.series.data);
        option.value.yAxis.max = Math.max(...option.value.series.data);
      }
      if (props.label == "Ingest Framerate (fps)") {
        option.value.series.data = Object.values(props.metrics).map((value) =>
          Math.trunc(value)
        );
        option.value.yAxis.min = Math.min(...option.value.series.data);
        option.value.yAxis.max = Math.max(...option.value.series.data);
      }
      if (props.label == "Keyframe Interval (idr)") {
        option.value.series.data = Object.values(props.metrics).map((value) =>
          Math.trunc(value)
        );
        option.value.yAxis.min = Math.min(...option.value.series.data);
        option.value.yAxis.max = Math.max(...option.value.series.data);
      }
      if (props.label == "Concurrent Views (count)") {
        option.value.series.data = Object.values(props.metrics).map((value) =>
          Math.trunc(value)
        );
        option.value.yAxis.min = Math.min(...option.value.series.data);
        option.value.yAxis.max = Math.max(...option.value.series.data);
      }
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
  height: 360px;
  margin: auto auto;
}
.echart {
  width: 100%;
  height: 360px;
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
