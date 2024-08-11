document.getElementById('fetch-tweet-button').addEventListener('click', async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/get_random_tweet/');
        const result = await response.json();

        if (result.tweet) {
            document.getElementById('input-text').value = result.tweet;
        } else {
            console.error('No tweet found in response.');
            document.getElementById('input-text').value = 'Error fetching tweet.';
        }
    } catch (error) {
        console.error('Error fetching tweet:', error);
        document.getElementById('input-text').value = 'Error fetching tweet.';
    }
});

document.getElementById('submit-button').addEventListener('click', async () => {
    // Show the overlay and loader
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
        
        // Display text tokens
        document.getElementById('response-text').textContent = JSON.stringify(result.text, null, 2);

        // Display explanation JSON
        document.getElementById('explanation-json').textContent = JSON.stringify(result.explanation_json, null, 2);

        // Parse explanation JSON
        result.explanation_json = JSON.parse(result.explanation_json);

        // Generate summary bar chart for general_sentiment
        const summaryBarChart = document.getElementById('summary-bar-chart');
        summaryBarChart.innerHTML = ''; // Clear previous content

        const generalSentiment = result.explanation_json.general_sentiment;
        if (generalSentiment) {
            const barContainer = document.createElement('div');
            barContainer.className = 'bar-container';

            const label = document.createElement('span');
            label.className = 'bar-label';
            label.textContent = 'Overall Sentiment';

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
            scoreLabel.textContent = `(${sentimentScore.toFixed(2)})`; // Display score with 2 decimal places

            barContainer.appendChild(label);
            barContainer.appendChild(bar);
            barContainer.appendChild(scoreLabel);
            summaryBarChart.appendChild(barContainer);
        } else {
            document.getElementById('response-text').textContent = 'General sentiment data is not available.';
        }

        // Clear previous word-level bars
        const barChart = document.getElementById('bar-chart');
        barChart.innerHTML = '';

        if (result.explanation_json && result.explanation_json.words) {
            // Create bars for each word in explanation
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
                scoreLabel.textContent = `(${sentimentScore.toFixed(2)})`; // Display score with 2 decimal places

                barContainer.appendChild(label);
                barContainer.appendChild(bar);
                barContainer.appendChild(scoreLabel);
                barChart.appendChild(barContainer);
            });
        } else {
            document.getElementById('response-text').textContent = 'Explanation data is not available.';
        }

        // Show LIME explanation link
        const limeLink = document.getElementById('lime-link');
        if (result.lime_explanation) {
            limeLink.href = result.lime_explanation;
            limeLink.textContent = 'View LIME Explanation';
        }

    } catch (error) {
        console.error('Error:', error);
        document.getElementById('response-text').textContent = 'Error fetching data.';
        document.getElementById('explanation-json').textContent = 'Error fetching explanation.';
    } finally {
        // Hide the overlay and loader
        document.getElementById('overlay').style.display = 'none';
        document.getElementById('loader').style.display = 'none';
    }
});
