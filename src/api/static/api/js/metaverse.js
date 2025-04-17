// Game constants
const TILE_SIZE = 32;
const PLAYER_SPEED = 3;
const ANIMATION_SPEED = 8; // Frames per animation cycle

// Game state
let playerX = 400;
let playerY = 300;
let playerId = Math.floor(Math.random() * 1000000);
let playerDirection = 'down'; // down, up, left, right
let playerFrame = 0;
let frameCount = 0;
let otherPlayers = {}; // Store other players' positions

// Assets
const assets = {
    player: {
        sprite: null,
        loaded: false,
        width: 32,
        height: 32,
        frames: 4, // Number of frames per direction
        directions: ['down', 'left', 'right', 'up']
    },
    tiles: {
        grass: null,
        loaded: false
    }
};

// Input handling
const keys = {};

// Canvas setup
const canvas = document.getElementById('game-canvas');
const ctx = canvas.getContext('2d');

// WebSocket setup
const wsScheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
const socket = new WebSocket(`${wsScheme}://${window.location.host}/ws/`);

socket.onopen = function(e) {
    console.log('WebSocket connection established');
    // Send initial player position
    sendPlayerPosition();
};

socket.onmessage = function(e) {
    console.log('Message received:', e.data);
    // Handle incoming messages (other players, map updates, etc.)
    if (e.data === 'pong!') {
        console.log('Received pong from server');
        return;
    }
    
    try {
        const data = JSON.parse(e.data);
        if (data.type === 'player_position' && data.player_id !== playerId) {
            // Update other player's position
            otherPlayers[data.player_id] = {
                x: data.x,
                y: data.y,
                direction: data.direction || 'down',
                frame: data.frame || 0
            };
        }
    } catch (error) {
        console.error('Error parsing WebSocket message:', error);
    }
};

socket.onclose = function(e) {
    console.log('WebSocket connection closed:', e);
};

function sendPlayerPosition() {
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            type: 'player_move',
            player_id: playerId,
            x: playerX,
            y: playerY,
            direction: playerDirection,
            frame: playerFrame
        }));
    }
}

// Load assets
function loadAssets() {
    // Load player sprite
    assets.player.sprite = new Image();
    assets.player.sprite.onload = function() {
        assets.player.loaded = true;
    };
    assets.player.sprite.src = '/static/api/images/character.png';
    
    // Load tile sprites
    assets.tiles.grass = new Image();
    assets.tiles.grass.onload = function() {
        assets.tiles.grass.loaded = true;
    };
    assets.tiles.grass.src = '/static/api/images/grass.png';
}

// Input event listeners
window.addEventListener('keydown', (e) => {
    keys[e.key] = true;
});

window.addEventListener('keyup', (e) => {
    keys[e.key] = false;
});

// Game loop
function gameLoop() {
    update();
    render();
    requestAnimationFrame(gameLoop);
}

function update() {
    // Handle player movement
    let moved = false;
    let oldX = playerX;
    let oldY = playerY;
    let oldDirection = playerDirection;
    
    if (keys['ArrowUp'] || keys['w']) {
        playerY -= PLAYER_SPEED;
        playerDirection = 'up';
        moved = true;
    } else if (keys['ArrowDown'] || keys['s']) {
        playerY += PLAYER_SPEED;
        playerDirection = 'down';
        moved = true;
    }
    
    if (keys['ArrowLeft'] || keys['a']) {
        playerX -= PLAYER_SPEED;
        playerDirection = 'left';
        moved = true;
    } else if (keys['ArrowRight'] || keys['d']) {
        playerX += PLAYER_SPEED;
        playerDirection = 'right';
        moved = true;
    }
    
    // Keep player within bounds
    playerX = Math.max(TILE_SIZE/2, Math.min(canvas.width - TILE_SIZE/2, playerX));
    playerY = Math.max(TILE_SIZE/2, Math.min(canvas.height - TILE_SIZE/2, playerY));
    
    // Update animation frame
    frameCount++;
    if (frameCount >= ANIMATION_SPEED) {
        frameCount = 0;
        if (moved) {
            playerFrame = (playerFrame + 1) % assets.player.frames;
        } else {
            playerFrame = 0; // Reset to standing frame when not moving
        }
    }
    
    // Send position update if player moved or changed direction
    if (moved || oldDirection !== playerDirection) {
        sendPlayerPosition();
    }
}

function render() {
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw background tiles
    drawBackground();
    
    // Draw grid (for development)
    drawGrid();
    
    // Draw other players
    for (const id in otherPlayers) {
        if (id !== playerId) {
            const player = otherPlayers[id];
            drawCharacter(
                player.x, 
                player.y, 
                player.direction, 
                player.frame
            );
        }
    }
    
    // Draw player
    drawCharacter(playerX, playerY, playerDirection, playerFrame);
}

function drawBackground() {
    if (!assets.tiles.grass.loaded) return;
    
    const tileSize = 32;
    for (let x = 0; x < canvas.width; x += tileSize) {
        for (let y = 0; y < canvas.height; y += tileSize) {
            ctx.drawImage(assets.tiles.grass, x, y, tileSize, tileSize);
        }
    }
}

function drawGrid() {
    ctx.strokeStyle = 'rgba(200, 200, 200, 0.3)';
    ctx.lineWidth = 1;
    
    // Draw vertical lines
    for (let x = 0; x <= canvas.width; x += TILE_SIZE) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
    }
    
    // Draw horizontal lines
    for (let y = 0; y <= canvas.height; y += TILE_SIZE) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
    }
}

function drawCharacter(x, y, direction, frame) {
    if (!assets.player.loaded) {
        // Fallback to circle if sprite not loaded
        ctx.fillStyle = '#3498db';
        ctx.beginPath();
        ctx.arc(x, y, TILE_SIZE/2, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#000';
        ctx.lineWidth = 2;
        ctx.stroke();
        return;
    }
    
    // Get the direction index
    const dirIndex = assets.player.directions.indexOf(direction);
    if (dirIndex === -1) return;
    
    // Calculate source rectangle in the sprite sheet
    const srcX = frame * assets.player.width;
    const srcY = dirIndex * assets.player.height;
    
    // Draw the character sprite
    ctx.drawImage(
        assets.player.sprite,
        srcX, srcY, assets.player.width, assets.player.height,
        x - assets.player.width/2, y - assets.player.height/2, 
        assets.player.width, assets.player.height
    );
}

// Initialize the game
function init() {
    loadAssets();
    gameLoop();
    
    // Ping the server every 30 seconds to keep the connection alive
    setInterval(() => {
        if (socket.readyState === WebSocket.OPEN) {
            socket.send('ping');
        }
    }, 30000);
}

// Start the game when the page loads
window.onload = init;
