document.getElementById('fetch-tweet-button').addEventListener('click', async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/get_random_tweet/');
        const result = await response.json();

        if (result.tweet) {
            document.getElementById('input-text').value = result.tweet;
        } else {
            console.error('Nijedna objava nije pronađena u odgovoru.');
            document.getElementById('input-text').value = 'Greška prilikom preuzimanja objave.';
        }
    } catch (error) {
        console.error('Greška prilikom preuzimanja objave:', error);
        document.getElementById('input-text').value = 'Greška prilikom preuzimanja objave.';
    }
});

document.getElementById('submit-button').addEventListener('click', async () => {
    // Pokaži overlay i loader
    document.getElementById('overlay').style.display = 'block';
    document.getElementById('loader').style.display = 'block';

    const inputText = document.getElementById('input-text').value;
    try {
        const response = await fetch('http://127.0.0.1:8000/predict/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: inputText })
        });

        const result = await response.json();
        
        // Prikaz tekstualnih tokena
        document.getElementById('response-text').textContent = JSON.stringify(result.text, null, 2);

        // Prikaz objašnjenja u JSON formatu
        document.getElementById('explanation-json').textContent = JSON.stringify(result.explanation_json, null, 2);

        // Parsiranje objašnjenja iz JSON formata
        result.explanation_json = JSON.parse(result.explanation_json);

        // Generisanje grafikona za opšti sentiment
        const summaryBarChart = document.getElementById('summary-bar-chart');
        summaryBarChart.innerHTML = ''; // Očisti prethodni sadržaj

        const generalSentiment = result.explanation_json.general_sentiment;
        if (generalSentiment) {
            const barContainer = document.createElement('div');
            barContainer.className = 'bar-container';

            const label = document.createElement('span');
            label.className = 'bar-label';
            label.textContent = 'Konačni rezultat';

            const bar = document.createElement('div');
            bar.className = 'bar';
            const sentimentScore = generalSentiment.score;
            bar.style.width = Math.abs(sentimentScore * 100) + '%';

            if (sentimentScore > 0) {
                bar.classList.add('positive');
            } else if (sentimentScore < 0) {
                bar.classList.add('negative');
            } else {
                bar.classList.add('neutral');
            }

            const scoreLabel = document.createElement('span');
            scoreLabel.className = 'score-label';
            scoreLabel.textContent = `(${sentimentScore.toFixed(2)})`; // Prikaz ocene sa 2 decimale

            barContainer.appendChild(label);
            barContainer.appendChild(bar);
            barContainer.appendChild(scoreLabel);
            summaryBarChart.appendChild(barContainer);
        } else {
            document.getElementById('response-text').textContent = 'Podaci o opštem sentimentu nisu dostupni.';
        }

        // Očisti prethodne grafikone za reči
        const barChart = document.getElementById('bar-chart');
        barChart.innerHTML = '';

        if (result.explanation_json && result.explanation_json.words) {
            // Kreiraj grafikone za svaku reč u objašnjenju
            result.explanation_json.words.forEach(word => {
                const barContainer = document.createElement('div');
                barContainer.className = 'bar-container';

                const label = document.createElement('span');
                label.className = 'bar-label';
                label.textContent = word.word;

                const bar = document.createElement('div');
                bar.className = 'bar';
                const sentimentScore = word.score;
                bar.style.width = Math.abs(sentimentScore * 100) + '%';

                if (sentimentScore > 0) {
                    bar.classList.add('positive');
                } else if (sentimentScore < 0) {
                    bar.classList.add('negative');
                } else {
                    bar.classList.add('neutral');
                }

                const scoreLabel = document.createElement('span');
                scoreLabel.className = 'score-label';
                scoreLabel.textContent = `(${sentimentScore.toFixed(2)})`; // Prikaz ocene sa 2 decimale

                barContainer.appendChild(label);
                barContainer.appendChild(bar);
                barContainer.appendChild(scoreLabel);
                barChart.appendChild(barContainer);
            });
        } else {
            document.getElementById('response-text').textContent = 'Podaci o objašnjenju nisu dostupni.';
        }

        // Prikaži link za LIME objašnjenje
        const limeLink = document.getElementById('lime-link');
        if (result.lime_explanation) {
            limeLink.href = result.lime_explanation;
            limeLink.textContent = 'Pogledaj LIME analizu';
            limeLink.classList.remove('disabled');
        }

    } catch (error) {
        console.error('Greška:', error);
        document.getElementById('response-text').textContent = 'Greška prilikom preuzimanja podataka.';
        document.getElementById('explanation-json').textContent = 'Greška prilikom preuzimanja objašnjenja.';
    } finally {
        // Sakrij overlay i loader
        document.getElementById('overlay').style.display = 'none';
        document.getElementById('loader').style.display = 'none';
    }
});
