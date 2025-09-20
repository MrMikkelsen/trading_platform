<script>
import { Pie } from "vue-chartjs";

export default {
  extends: Pie,
  props: {
    chartData: {
      type: Object,
      default: null,
    },
    options: {
      type: Object,
      default: null,
    },
    pieChartRenderVersion: {
      type : Number,
    },
  },

  mounted() {
    this.renderChart(this.chartData, this.options);
  },
  watch: {
    pieChartRenderVersion: function(){
      this.renderChart(this.chartData, this.options);
    }
  }
};
</script>
