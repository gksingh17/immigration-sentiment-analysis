import Papa from 'papaparse';

import { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import BarChart from './BarChart'

ChartJS.register( 
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
)
function App() {

  const [chartData,setChartData ] = useState({
    datasets: []
  });
  const [charOptions, setChartOptions] = useState({})

  useEffect(() => {
    // Papa.parse(YoutubeData, {
    //   download: true,
    //   header:true,
    //   dynamicTyping:true,
    //   delimiter:"",
    //   complete:((result) => {
    //     console.log(result)
    //   })
    // })


  }, [])

  return (
    <div className="App">
      <BarChart />
    </div>
  );
}

export default App;
