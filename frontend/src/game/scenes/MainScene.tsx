import Phaser from 'phaser';
import axios from 'axios';

export default class MainScene extends Phaser.Scene {
  private player!: Phaser.Physics.Arcade.Sprite;
  private cursors!: Phaser.Types.Input.Keyboard.CursorKeys;
  private spaceElements: Phaser.GameObjects.Sprite[] = [];
  private socket!: WebSocket;

  constructor() {
    super({ key: 'MainScene' });
  }

  preload() {
    // Load player avatar
    this.load.image('player', '/static/avatars/default.png');
    
    // Load space elements
    this.load.image('chair', '/static/elements/chair.png');
    this.load.image('table', '/static/elements/table.png');
  }

  async create() {
    // Initialize WebSocket connection
    this.socket = new WebSocket('ws://localhost:8000/ws/metaverse/');
    
    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.handleWebSocketMessage(data);
    };

    // Create player
    this.player = this.physics.add.sprite(400, 300, 'player');
    this.player.setCollideWorldBounds(true);

    // Set up keyboard input
    this.cursors = this.input.keyboard.createCursorKeys();

    // Load space elements
    await this.loadSpaceElements();

    // Set up collisions
    this.physics.add.collider(this.player, this.spaceElements);
  }

  async loadSpaceElements() {
    try {
      const response = await axios.get('/api/spaces/all/');
      const spaces = response.data;

      spaces.forEach((space: any) => {
        const element = this.physics.add.sprite(
          space.x * 32,
          space.y * 32,
          space.element.type
        );
        this.spaceElements.push(element);
      });
    } catch (error) {
      console.error('Error loading space elements:', error);
    }
  }

  handleWebSocketMessage(data: any) {
    // Handle real-time updates from other players
    if (data.type === 'player_move') {
      // Update other player positions
    } else if (data.type === 'chat') {
      // Handle chat messages
    }
  }

  update() {
    // Handle player movement
    const speed = 160;
    const playerBody = this.player.body as Phaser.Physics.Arcade.Body;

    if (this.cursors.left.isDown) {
      playerBody.setVelocityX(-speed);
    } else if (this.cursors.right.isDown) {
      playerBody.setVelocityX(speed);
    } else {
      playerBody.setVelocityX(0);
    }

    if (this.cursors.up.isDown) {
      playerBody.setVelocityY(-speed);
    } else if (this.cursors.down.isDown) {
      playerBody.setVelocityY(speed);
    } else {
      playerBody.setVelocityY(0);
    }

    // Send player position to server
    if (this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify({
        type: 'player_move',
        x: this.player.x,
        y: this.player.y
      }));
    }
  }
} 