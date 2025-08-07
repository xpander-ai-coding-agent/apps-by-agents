// Rick and Morty quotes for different difficulty levels
const quotes = {
    easy: [
        "Wubba lubba dub dub!",
        "I'm Pickle Rick!",
        "Nobody exists on purpose.",
        "Get your shit together.",
        "This is getting weird.",
        "Don't think about it.",
        "I'm Mr. Meeseeks!",
        "Show me what you got!",
        "Grass tastes bad.",
        "Existence is pain."
    ],
    medium: [
        "Listen, Morty, I hate to break it to you, but what people call love is just a chemical reaction.",
        "Sometimes science is more art than science, Morty. A lot of people don't get that.",
        "I turned myself into a pickle, Morty! I'm Pickle Rick!",
        "The universe is basically an animal. It grazes on the ordinary.",
        "You're young, you have your whole life ahead of you, and your anal cavity is still taut yet malleable.",
        "School is not a place for smart people, Morty.",
        "Weddings are basically funerals with cake.",
        "Nobody exists on purpose, nobody belongs anywhere, everybody's gonna die. Come watch TV.",
        "Having a family doesn't mean that you stop being an individual.",
        "To live is to risk it all; otherwise you're just an inert chunk of randomly assembled molecules."
    ],
    hard: [
        "Listen, I'm not the nicest guy in the universe, because I'm the smartest, and being nice is something stupid people do to hedge their bets.",
        "The universe is basically an animal. It grazes on the ordinary. It creates infinite idiots just to eat them.",
        "When you know nothing matters, the universe is yours. And I've never met a universe that was into it.",
        "Scientifically, traditions are an idiot thing. But I'll be damned if I'm not eating a turkey dinner with my family.",
        "You don't get to tell me what's important! You're not my therapist, Jerry! And you're not licensed to be anyone's therapist!",
        "I'm not looking for judgement, just a yes or no. Can you assimilate a giraffe?",
        "The thing about repairing, maintaining, and cleaning is it's not an adventure. There's no way to do it so wrong you might die.",
        "Well then get your shit together, get it all together and put it in a backpack, all your shit, so it's together.",
        "You can't just add a sci-fi word to a car word and hope it means something.",
        "I don't like it here Morty. I can't abide bureaucracy. I don't like being told where to go and what to do."
    ]
};

// Rick's comments based on performance
const rickComments = {
    excellent: [
        "Holy shit, Morty! You're typing faster than I can burp!",
        "Not bad for a human. Still slower than my portal gun though.",
        "Wubba lubba dub dub! That's what I call typing!",
        "You must have some Rick DNA in you. Jerry sure doesn't type like that."
    ],
    good: [
        "Decent work, Morty. You're almost as fast as Summer texting her friends.",
        "Not terrible. I've seen worse from entire civilizations.",
        "You're getting there. Keep practicing and maybe you'll be useful someday."
    ],
    average: [
        "Meh. That's about what I'd expect from someone in this dimension.",
        "You type like Jerry thinks - slowly and with lots of mistakes.",
        "I've seen Cronenbergs type faster than that."
    ],
    poor: [
        "Jesus, Morty! Did you type that with your feet?",
        "This is painful to watch. Like Jerry trying to understand quantum physics.",
        "Are you having a stroke? Should I call Space Beth?",
        "I've seen better typing from a Plumbus."
    ]
};

// Game state
let gameState = {
    isRunning: false,
    currentQuote: '',
    typedText: '',
    startTime: null,
    timeRemaining: 60,
    timerInterval: null,
    correctChars: 0,
    totalChars: 0,
    difficulty: 'medium'
};

// DOM elements
const quoteDisplay = document.getElementById('quoteDisplay');
const quoteInput = document.getElementById('quoteInput');
const wpmDisplay = document.getElementById('wpm');
const accuracyDisplay = document.getElementById('accuracy');
const timerDisplay = document.getElementById('timer');
const startBtn = document.getElementById('startBtn');
const resetBtn = document.getElementById('resetBtn');
const difficultySelect = document.getElementById('difficulty');
const resultsDiv = document.getElementById('results');
const rickPortal = document.getElementById('rickPortal');

// Event listeners
startBtn.addEventListener('click', startTest);
resetBtn.addEventListener('click', resetTest);
quoteInput.addEventListener('input', handleInput);
difficultySelect.addEventListener('change', (e) => {
    gameState.difficulty = e.target.value;
});

// Mouse portal effect
document.addEventListener('mousemove', (e) => {
    if (gameState.isRunning) {
        rickPortal.style.left = e.clientX - 50 + 'px';
        rickPortal.style.top = e.clientY - 50 + 'px';
        rickPortal.classList.add('active');
    }
});

// Start the test
function startTest() {
    gameState.isRunning = true;
    gameState.startTime = Date.now();
    gameState.timeRemaining = 60;
    gameState.correctChars = 0;
    gameState.totalChars = 0;
    gameState.typedText = '';
    
    // Get random quote
    const difficultyQuotes = quotes[gameState.difficulty];
    gameState.currentQuote = difficultyQuotes[Math.floor(Math.random() * difficultyQuotes.length)];
    
    // Update UI
    displayQuote();
    quoteInput.disabled = false;
    quoteInput.value = '';
    quoteInput.focus();
    startBtn.disabled = true;
    resetBtn.disabled = false;
    resultsDiv.style.display = 'none';
    quoteDisplay.classList.add('active');
    
    // Start timer
    updateTimer();
    gameState.timerInterval = setInterval(updateTimer, 1000);
}

// Reset the test
function resetTest() {
    gameState.isRunning = false;
    clearInterval(gameState.timerInterval);
    
    // Reset UI
    quoteDisplay.textContent = 'Click "Start Test" to begin your interdimensional typing adventure!';
    quoteDisplay.classList.remove('active');
    quoteInput.value = '';
    quoteInput.disabled = true;
    startBtn.disabled = false;
    resetBtn.disabled = true;
    wpmDisplay.textContent = '0';
    accuracyDisplay.textContent = '100%';
    timerDisplay.textContent = '60s';
    resultsDiv.style.display = 'none';
    rickPortal.classList.remove('active');
}

// Display quote with formatting
function displayQuote() {
    quoteDisplay.innerHTML = gameState.currentQuote
        .split('')
        .map((char, index) => `<span class="char-${index}">${char}</span>`)
        .join('');
}

// Handle input
function handleInput(e) {
    if (!gameState.isRunning) return;
    
    const inputValue = e.target.value;
    gameState.typedText = inputValue;
    
    // Update character highlighting
    const quoteChars = gameState.currentQuote.split('');
    const inputChars = inputValue.split('');
    
    let correct = 0;
    let total = inputChars.length;
    
    quoteChars.forEach((char, index) => {
        const charSpan = quoteDisplay.querySelector(`.char-${index}`);
        
        if (index < inputChars.length) {
            if (inputChars[index] === char) {
                charSpan.classList.add('correct');
                charSpan.classList.remove('incorrect', 'current');
                correct++;
            } else {
                charSpan.classList.add('incorrect');
                charSpan.classList.remove('correct', 'current');
            }
        } else if (index === inputChars.length) {
            charSpan.classList.add('current');
            charSpan.classList.remove('correct', 'incorrect');
        } else {
            charSpan.classList.remove('correct', 'incorrect', 'current');
        }
    });
    
    gameState.correctChars = correct;
    gameState.totalChars = total;
    
    // Update stats
    updateStats();
    
    // Check if quote is completed
    if (inputValue === gameState.currentQuote) {
        // Get new quote
        const difficultyQuotes = quotes[gameState.difficulty];
        let newQuote;
        do {
            newQuote = difficultyQuotes[Math.floor(Math.random() * difficultyQuotes.length)];
        } while (newQuote === gameState.currentQuote);
        
        gameState.currentQuote = newQuote;
        displayQuote();
        quoteInput.value = '';
        gameState.typedText = '';
        
        // Add a little celebration effect
        quoteDisplay.style.animation = 'none';
        setTimeout(() => {
            quoteDisplay.style.animation = '';
        }, 10);
    }
}

// Update timer
function updateTimer() {
    gameState.timeRemaining--;
    timerDisplay.textContent = `${gameState.timeRemaining}s`;
    
    if (gameState.timeRemaining <= 0) {
        endTest();
    }
}

// Update stats
function updateStats() {
    // Calculate WPM
    const timeElapsed = (Date.now() - gameState.startTime) / 1000 / 60; // in minutes
    const wordsTyped = gameState.correctChars / 5; // standard word length
    const wpm = Math.round(wordsTyped / timeElapsed) || 0;
    
    // Calculate accuracy
    const accuracy = gameState.totalChars > 0 
        ? Math.round((gameState.correctChars / gameState.totalChars) * 100) 
        : 100;
    
    wpmDisplay.textContent = wpm;
    accuracyDisplay.textContent = `${accuracy}%`;
}

// End test
function endTest() {
    gameState.isRunning = false;
    clearInterval(gameState.timerInterval);
    
    // Calculate final stats
    const finalWpm = parseInt(wpmDisplay.textContent);
    const finalAccuracy = parseInt(accuracyDisplay.textContent);
    
    // Update results
    document.getElementById('finalWpm').textContent = finalWpm;
    document.getElementById('finalAccuracy').textContent = `${finalAccuracy}%`;
    document.getElementById('totalChars').textContent = gameState.correctChars;
    
    // Get Rick's comment
    let commentCategory;
    if (finalWpm >= 80 && finalAccuracy >= 95) {
        commentCategory = 'excellent';
    } else if (finalWpm >= 60 && finalAccuracy >= 85) {
        commentCategory = 'good';
    } else if (finalWpm >= 40 && finalAccuracy >= 75) {
        commentCategory = 'average';
    } else {
        commentCategory = 'poor';
    }
    
    const comments = rickComments[commentCategory];
    const randomComment = comments[Math.floor(Math.random() * comments.length)];
    document.getElementById('rickComment').textContent = `"${randomComment}" - Rick`;
    
    // Show results
    resultsDiv.style.display = 'block';
    quoteInput.disabled = true;
    startBtn.disabled = false;
    resetBtn.disabled = false;
    quoteDisplay.classList.remove('active');
    rickPortal.classList.remove('active');
}