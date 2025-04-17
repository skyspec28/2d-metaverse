import React, { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import Phaser from 'phaser';
import { Box, Typography, Button } from '@mui/material';
import axios from 'axios';

// Game scenes
import MainScene from '../game/scenes/MainScene';

const Metaverse: React.FC = () => {
  const gameRef = useRef<Phaser.Game | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const config: Phaser.Types.Core.GameConfig = {
      type: Phaser.AUTO,
      width: window.innerWidth,
      height: window.innerHeight,
      parent: 'game-container',
      scene: [MainScene],
      physics: {
        default: 'arcade',
        arcade: {
          gravity: { y: 0 },
          debug: false
        }
      }
    };

    gameRef.current = new Phaser.Game(config);

    return () => {
      if (gameRef.current) {
        gameRef.current.destroy(true);
      }
    };
  }, []);

  const handleCreateSpace = async () => {
    try {
      const response = await axios.post('/api/spaces/new/', {
        name: 'New Space',
        width: 800,
        height: 600,
        map: 1 // Default map ID
      });
      
      navigate(`/space/${response.data.space_id}`);
    } catch (error) {
      console.error('Error creating space:', error);
    }
  };

  return (
    <Box sx={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ p: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4">2D Metaverse</Typography>
        <Button variant="contained" onClick={handleCreateSpace}>
          Create New Space
        </Button>
      </Box>
      <Box id="game-container" sx={{ flex: 1 }} />
    </Box>
  );
};

export default Metaverse; 