document.addEventListener('DOMContentLoaded', function() {
    const images = [
        {src: 'b_rumpsteak.jpg', retailCut: 'Rump Steak', species: 'Beef', primal: 'Rump'},
        {src: 'b_rumpsteak7.jpg', retailCut: 'Rump Steak', species: 'Beef', primal: 'Rump'},
        {src: 'b_rumpsteak8.jpg', retailCut: 'Rump Steak', species: 'Beef', primal: 'Rump'},
        {src: 'b_shinbeefbonein.jpg', retailCut: 'Shin Beef Bone-in', species: 'Beef', primal: 'Shin'},
        {src: 'b_shinbeefboneless2.jpg', retailCut: 'Shin Beef Boneless', species: 'Beef', primal: 'Shin'}
    ];

    let currentImageIndex = -1;

    const meatImage = document.getElementById('meat-image');
    const resultDiv = document.getElementById('result');
    const nextBtn = document.getElementById('next-btn');
    const answerBtn = document.getElementById('answer-btn');
    const retailCutInput = document.getElementById('retail-cut-name');
    const speciesInput = document.getElementById('species');
    const primalInput = document.getElementById('primal-name');

    nextBtn.addEventListener('click', loadRandomImage);
    answerBtn.addEventListener('click', checkAnswer);

    function loadRandomImage() {
        currentImageIndex = Math.floor(Math.random() * images.length);
        meatImage.src = images[currentImageIndex].src;
        resultDiv.textContent = '';
        retailCutInput.value = '';
        speciesInput.value = '';
        primalInput.value = '';
    }

    function checkAnswer() {
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

    // Load the first random image on page load
    loadRandomImage();
});
