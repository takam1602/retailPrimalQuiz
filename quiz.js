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
    Papa.parse('retailIndex_utf8.csv', {
        download: true,
        header: true,
        skipEmptyLines: true,
        complete: function(results) {
            console.log("CSV読み込み完了:", results); 
            if (results.errors.length > 0) {
                console.error("CSVパースエラー:", results.errors); 
                results.errors.forEach(error => {
                    console.error("エラーの詳細:", error);
                });
                return;
            }
            images = results.data;
            console.log("パースされたデータ:", images); 
            loadRandomImage();
        },
        error: function(error) {
            console.error("CSV読み込みエラー:", error); 
        }
    });

    nextBtn.addEventListener('click', loadRandomImage);
    answerBtn.addEventListener('click', checkAnswer);

    let currentImageIndex = -1;

    function loadRandomImage() {
        if (images.length > 0) {
            currentImageIndex = Math.floor(Math.random() * images.length);
            const selectedImage = images[currentImageIndex];
            console.log("選択された画像データ:", selectedImage); 
            if (selectedImage && selectedImage.src) {
                meatImage.src = selectedImage.src;
            } else {
                console.error("画像データが不正です:", selectedImage); 
                meatImage.src = "";
            }
            resultDiv.textContent = '';
            retailCutInput.value = '';
            speciesInput.value = '';
            primalInput.value = '';
        } else {
            console.error("画像データがありません");
        }
    }
    function normalizeInput(input) {
    return input.trim().toLowerCase().replace(/[\s\u3000]+/g, ' ');
    }

    function checkAnswer() {
    if (currentImageIndex === -1) return;

    const retailCut = normalizeInput(retailCutInput.value);
    const species = normalizeInput(speciesInput.value);
    const primal = normalizeInput(primalInput.value);

    const correctData = images[currentImageIndex];

    const correctRetailCut = normalizeInput(correctData.retailCut);
    const correctSpecies = normalizeInput(correctData.species);
    const correctPrimal = normalizeInput(correctData.primal);

    if (retailCut === correctRetailCut &&
        species === correctSpecies &&
        primal === correctPrimal) {
        resultDiv.textContent = 'Correct!';
    } else {
        resultDiv.textContent = `Incorrect. The correct answers are:\n
        Retail Cut: ${correctData.retailCut}\n
        Species: ${correctData.species}\n
        Primal: ${correctData.primal}`;
    }
    }   
});
