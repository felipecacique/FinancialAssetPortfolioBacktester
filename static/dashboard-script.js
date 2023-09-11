// Wait of the DOM to fully load
document.addEventListener("DOMContentLoaded", () => {
    console.log("DOMContentLoaded");
    // Get form, buttons, and error message elements
    const logoutButton = document.getElementById("logout-button");
    const usernamePlaceholder = document.getElementById("username-placeholder");

    // Add a click event listener to the logout button
    logoutButton.addEventListener("click", async () => {
        console.log("logoutButton click");
        try {
            const response = await fetch("/logout", {
                method: "GET"
            });

            console.log(response);

            if (response.ok) {
                console.log("Logged out");
                // Redirect to the index page after logout
                window.location.href = "/";
            } else {
                console.error("Logout failed:", response.status);
            }
        } catch (error) {
            console.error("Error:", error);
        }
    });

    
    const loadTableButton = document.getElementById("loadTable");
    loadTableButton.addEventListener('click', async function () {
        const params = {
            "liquidezMin": 1000000,
            "fatorEvEbit": 1,
            "fatorRoic": 1,
            "fatorRetornoMensal": 1,
            "rankingQtd": 10
        };
        data = await getPortfolio(params)

        console.log("data: ", data)

        if (data.success) {

            // Sample data for the portfolio table
            // const tableData = [
            //     { asset: 'Stocks', value: '$30,000' },
            //     { asset: 'Bonds', value: '$25,000' },
            //     { asset: 'Real Estate', value: '$150,000' },
            //     { asset: 'Cash', value: '$5,000' }
            // ];

            let tableData = [];
            data.resultado.forEach(item => {
                // const row = {asset: item.Papel, value: item.ranking_total}
                const row = item
                tableData.push(row)
            });
        
            const tableBody = document.getElementById('portfolioTableBody');

            // Remove all existing rows
            if (tableBody) {
                while (tableBody.firstChild) {
                    tableBody.removeChild(tableBody.firstChild);
                }
            }

            // Populate the portfolio table
            tableData.forEach((item,index) => {
                const row = document.createElement('tr');
                row.innerHTML = `<td>${index+1}</td><td>${item['Papel']}</td><td>${item['Cotação']}</td><td>${item['EV/EBIT']}</td><td>${item['ROIC']}</td><td>${item['Liq.2meses']}</td><td>${item['ranking_total']}</td>`;
                tableBody.appendChild(row);
            });

            
            // Initialize DataTables for the portfolio table
            $(document).ready(function () {
                $('#portfolioTable').DataTable();
            });


            const ctx = document.getElementById('portfolioChart').getContext('2d');

            let portfolioChart;

            function plotPortfolioChart() {
                if (portfolioChart) {
                    portfolioChart.destroy();
                }

                // create a list with the top 10 assets of the ranking
                let assets = []
                for (let i = 0; i < Math.min(tableData.length, 10); i ++) {
                    assets.push(tableData[i]['Papel'])
                }
                console.log(`Assets list: ${assets}`)

                const chartData = {
                    labels: assets,
                    datasets: [{
                        data: [100/10, 100/10, 100/10, 100/10, 100/10, 100/10, 100/10, 100/10, 100/10, 100/10],
                        backgroundColor: ["#0074D9", "#FF4136", "#2ECC40", "#FF851B", "#7FDBFF", 
                        "#B10DC9", "#FFDC00", "#001f3f", "#39CCCC", "#01FF70", "#85144b", "#F012BE", 
                        "#3D9970", "#111111", "#AAAAAA"]
                    }]
                };
                // Create and render the chart
                portfolioChart = new Chart(ctx, {
                    type: 'doughnut',
                    data: chartData
                });
            }
         
            plotPortfolioChart();
 
        }

    });


    // Handle checkbox changes
    const liquidityCheckbox = document.getElementById('liquidityCheckbox');
    const fatorEvEbitCheckbox = document.getElementById('fatorEvEbitCheckbox');
    const fatorRoicCheckbox = document.getElementById('fatorRoicCheckbox');
    const fatorRetornoMensalCheckbox = document.getElementById('fatorRetornoMensalCheckbox');
    const rankingQtdCheckbox = document.getElementById('rankingQtdCheckbox');

    const liquidityContainer = document.querySelector('#liquidityContainer');
    const fatorEvEbitContainer = document.querySelector('#fatorEvEbitContainer');
    const fatorRoicContainer = document.querySelector('#fatorRoicContainer');
    const fatorRetornoMensalContainer = document.querySelector('#fatorRetornoMensalContainer');
    const rankingQtdContainer = document.querySelector('#rankingQtdContainer');       

    const liquidityInput = document.getElementById('liquidityInput');
    const fatorEvEbitInput = document.getElementById('fatorEvEbitInput');
    const fatorRoicInput = document.getElementById('fatorRoicInput');
    const fatorRetornoMensalInput = document.getElementById('fatorRetornoMensalInput');
    const rankingQtdInput = document.getElementById('rankingQtdInput');
    
    // Initial values
    liquidityInput.value = 1000000;
    fatorEvEbitInput.value = 1.;
    fatorRoicInput.value = 1.;
    fatorRetornoMensalInput.value = 1.;
    rankingQtdInput.value = 10;

    const errorMessage = document.getElementById('input-error-message');
    
    liquidityCheckbox.addEventListener('change', function() {
        if (this.checked) {
            liquidityContainer.style.display = 'block';
        } else {
            liquidityContainer.style.display = 'none';
        }
    });

    fatorEvEbitCheckbox.addEventListener('change', function() {
        if (this.checked) {
            fatorEvEbitContainer.style.display = 'block';
        } else {
            fatorEvEbitContainer.style.display = 'none';
        }
    });

    fatorRoicCheckbox.addEventListener('change', function() {
        if (this.checked) {
            fatorRoicContainer.style.display = 'block';
        } else {
            fatorRoicContainer.style.display = 'none';
        }
    });

    fatorRetornoMensalCheckbox.addEventListener('change', function() {
        if (this.checked) {
            fatorRetornoMensalContainer.style.display = 'block';
        } else {
            fatorRetornoMensalContainer.style.display = 'none';
        }
    });

    rankingQtdCheckbox.addEventListener('change', function() {
        if (this.checked) {
            rankingQtdContainer.style.display = 'block';
        } else {
            rankingQtdContainer.style.display = 'none';
        }
    });

    if (isNumber(liquidityInput) | isNumber(fatorEvEbitInput))
    {
        errorMessage.textContent = "Fields must contain numbers";
    }


    liquidityInput.addEventListener('input', function() {
        if (textInput.value !== '' && !isNumber(textInput.value)) {
            textInput.setCustomValidity('Enter a number');
            errorMessage.textContent = "Fields must contain numbers";
        } else {
            textInput.setCustomValidity('');
        }
        if (isNumber(liquidityInput.value))
        {
            errorMessage.textContent = "Fields must contain numbers";
        }
        errorMessage.textContent = "Fields must contain numbersss";
    });


    function isNumber(value) {
        return /^[+-]?\d+(\.\d+)?$/.test(value);
    }
    

    // Sample data for the time series chart
    const timeSeriesData = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        datasets: [
            {
                label: 'Stock Price',
                data: [150, 160, 170, 180, 190],
                borderColor: '#FF5733',
                fill: false,
                hidden: false // Initial visibility state
            },
            {
                label: 'Bond Price',
                data: [100, 110, 105, 115, 120],
                borderColor: '#36A2EB',
                fill: false,
                hidden: false // Initial visibility state
            },
            {
                label: 'Real Estate Price',
                data: [200, 210, 220, 230, 240],
                borderColor: '#4CAF50',
                fill: false,
                hidden: false // Initial visibility state
            },
        ]
    };

    // Initialize and render the time series chart
    const timeSeriesCtx = document.getElementById('timeSeriesChart').getContext('2d');
    let timeSeriesChart;

    // LOad time series data and handle checkbox changes
    const loadTimeSeriesButton = document.getElementById('loadTimeSeriesData');


    loadTimeSeriesButton.addEventListener('click', async function () {
        

        // First lets process the input values
        if (!isNumber(liquidityInput.value) | !isNumber(fatorEvEbitInput.value) | 
            !isNumber(fatorRoicInput.value) | !isNumber(fatorRetornoMensalInput.value) | 
            !isNumber(rankingQtdInput.value))
        {
            errorMessage.textContent = "Fields must contain numbers";
            return ;
        }

        // const params = {
        //     "liquidezMin": 1000000,
        //     "fatorEvEbit": 1,
        //     "fatorRoic": 1,
        //     "fatorRetornoMensal": 1,
        //     "rankingQtd": 10
        // };

        const params = {
            "liquidezMin": parseFloat(liquidityInput.value),
            "fatorEvEbit": parseFloat(fatorEvEbitInput.value),
            "fatorRoic": parseFloat(fatorRoicInput.value),
            "fatorRetornoMensal": parseFloat(fatorRetornoMensalInput.value),
            "rankingQtd": parseFloat(rankingQtdInput.value),
        };

        errorMessage.textContent = "";
        
        if (timeSeriesChart) {
            timeSeriesChart.destroy();
        }

        console.log("Calling getDataFromModel!");

        // Get data from criadnoUmModeloDeInvestimento API
        data = await getDataFromModel(params)

        console.log("Data:", data);
        
        if (data.success){
            plotTimeSeriesData(data);
        }
        
    });


    // Function to get data from criadnoUmModeloDeInvestimento API
    async function getDataFromModel(params) {
        try {
            const response = await fetch ("/criandoUmModeloDeInvestimento", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(params)
            });
            
            const data = await response.json();
            console.log(data);
            if (data.success){
                console.log("getDataFromModel successful!");
            }
            else {
                console.log("getDataFromModel not successful!");
            }
            return data;
        }
        catch (error) {
            console.error('Error:', error);
            return null;
        }
    }


    // Function to plot data using Chart.js
    function plotTimeSeriesData(data) {
        // Lets plot the graph
        const timeSeriesData = {
            labels: data.resultado.timeSeriesData.labels,
            datasets: [
                {
                    label: 'Modelo',
                    data: data.resultado.timeSeriesData.datasets[0].data,
                    borderColor: '#FF5733',
                    fill: false,
                    hidden: false // Initial visibility state
                },
                {
                    label: 'Ibov',
                    data: data.resultado.timeSeriesData.datasets[1].data,
                    borderColor: '#36A2EB',
                    fill: false,
                    hidden: false // Initial visibility state
                }
            ]
        };

        timeSeriesChart = new Chart(timeSeriesCtx, {
            type: 'line',
            data: timeSeriesData,
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });       
    }


    // Function to get data from pegadoDadosEmSitesAutomatizarCriacaoCarteira API
    async function getPortfolio(params) {
        try {
            const response = await fetch ("/pegadoDadosEmSitesAutomatizarCriacaoCarteira", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(params)
            });
            
            const data = await response.json();
            console.log(data);
            if (data.success){
                console.log("getPortfolio successful!");
            }
            else {
                console.log("getPortfolio not successful!");
            }
            return data;
        }
        catch (error) {
            console.error('Error:', error);
            return null;
        }
    }

});
