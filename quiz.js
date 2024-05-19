document.addEventListener('DOMContentLoaded', function() {
    let images = [];
    const meatImage = document.getElementById('meat-image');
    const resultDiv = document.getElementById('result');
    const nextBtn = document.getElementById('next-btn');
    const answerBtn = document.getElementById('answer-btn');
    const retailCutInput = document.getElementById('retail-cut-name');
    const speciesInput = document.getElementById('species');
    const primalInput = document.getElementById('primal-name');

    // CSVファイルの読み込みと解析
    Papa.parse('retailIndex.csv', {
        download: true,
        header: true,
        complete: function(results) {
            images = results.data;
            loadRandomImage();
        }
    });

    nextBtn.addEventListener('click', loadRandomImage);
    answerBtn.addEventListener('click', checkAnswer);

    let currentImageIndex = -1;

    function loadRandomImage() {
        if (images.length > 0) {
            currentImageIndex = Math.floor(Math.random() * images.length);
            meatImage.src = images[currentImageIndex].src;
            resultDiv.textContent = '';
            retailCutInput.value = '';
            speciesInput.value = '';
            primalInput.value = '';
        }
    }

    function checkAnswer() {
        if (currentImageIndex === -1) return;

        const retailCut = retailCutInput.value.trim();
        const species = speciesInput.value.trim();
        const primal = primalInput.value.trim();

        const correctData = images[currentImageIndex];

        if (retailCut.toLowerCase() === correctData.retailCut.toLowerCase() &&
            species.toLowerCase() === correctData.species.toLowerCase() &&
            primal.toLowerCase() === correctData.primal.toLowerCase()) {
            resultDiv.textContent = 'Correct!';
        } else {
            resultDiv.textContent = `Incorrect. The correct answers are:
            Retail Cut: ${correctData.retailCut},
            Species: ${correctData.species},
            Primal: ${correctData.primal}`;
        }
    }
});
