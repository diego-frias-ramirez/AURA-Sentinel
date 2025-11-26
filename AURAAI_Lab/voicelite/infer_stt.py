"""
AuraVoiceLite - Speech-to-Text Inference
Production-grade STT inference using Whisper for emergency voice recognition.
Optimized for Spanish (Mexico) with medical/emergency terminology support.

Author: AuraAI_Lab
Version: 1.0.0
"""

import numpy as np
import torch
import torchaudio
import os
import json
import logging
import argparse
from datetime import datetime
from typing import Dict, Optional
import warnings
warnings.filterwarnings('ignore')

try:
    from transformers import WhisperProcessor, WhisperForConditionalGeneration
except ImportError:
    print("Error: transformers library not installed.")
    print("Install with: pip install transformers torch torchaudio")
    exit(1)

# Paths
MODEL_CACHE_DIR = 'models/whisper_cache'
CONFIG_PATH = 'models/stt_config.json'
INFERENCE_LOG = 'models/stt_inference.log'

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(INFERENCE_LOG),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class VoiceLiteSTT:
    """Production STT engine using Whisper"""
    
    # Model configurations
    MODEL_CONFIGS = {
        'tiny': {
            'model_id': 'openai/whisper-tiny',
            'size_mb': 39,
            'speed': 'muy rápido',
            'quality': 'básica',
            'recommended_for': 'testing rápido'
        },
        'base': {
            'model_id': 'openai/whisper-base',
            'size_mb': 74,
            'speed': 'rápido',
            'quality': 'buena',
            'recommended_for': 'dispositivos móviles'
        },
        'small': {
            'model_id': 'openai/whisper-small',
            'size_mb': 244,
            'speed': 'medio',
            'quality': 'muy buena',
            'recommended_for': 'equilibrio calidad-velocidad'
        },
        'medium': {
            'model_id': 'openai/whisper-medium',
            'size_mb': 769,
            'speed': 'lento',
            'quality': 'excelente',
            'recommended_for': 'máxima precisión'
        }
    }
    
    def __init__(self, model_size: str = 'base', device: Optional[str] = None):
        """
        Initialize STT engine
        
        Args:
            model_size: Whisper model size ('tiny', 'base', 'small', 'medium')
            device: Device to use ('cuda', 'cpu', or None for auto-detect)
        """
        self.model_size = model_size
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.processor = None
        self.model = None
        self.is_loaded = False
        
        logger.info("VoiceLite STT initialized")
        logger.info("Model size: %s", model_size)
        logger.info("Device: %s", self.device)
    
    def load_model(self):
        """Load Whisper model and processor"""
        logger.info("Loading Whisper model...")
        
        if self.model_size not in self.MODEL_CONFIGS:
            raise ValueError(f"Invalid model size. Choose from: {list(self.MODEL_CONFIGS.keys())}")
        
        model_id = self.MODEL_CONFIGS[self.model_size]['model_id']
        
        try:
            # Load processor
            logger.info("Loading processor from: %s", model_id)
            self.processor = WhisperProcessor.from_pretrained(
                model_id,
                cache_dir=MODEL_CACHE_DIR
            )
            
            # Load model
            logger.info("Loading model from: %s", model_id)
            self.model = WhisperForConditionalGeneration.from_pretrained(
                model_id,
                cache_dir=MODEL_CACHE_DIR
            ).to(self.device)
            
            # Set to evaluation mode
            self.model.eval()
            
            # Force Spanish language
            self.model.config.forced_decoder_ids = self.processor.get_decoder_prompt_ids(
                language="spanish",
                task="transcribe"
            )
            
            self.is_loaded = True
            logger.info("Model loaded successfully")
            logger.info("Configured for Spanish (Mexico)")
            
        except Exception as e:
            logger.error("Failed to load model: %s", str(e))
            raise
    
    def load_audio(self, audio_path: str) -> torch.Tensor:
        """
        Load and preprocess audio file
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Preprocessed audio tensor
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        logger.info("Loading audio: %s", audio_path)
        
        # Load audio
        waveform, sample_rate = torchaudio.load(audio_path)
        
        # Convert to mono if stereo
        if waveform.shape[0] > 1:
            waveform = torch.mean(waveform, dim=0, keepdim=True)
        
        # Resample to 16kHz (Whisper requirement)
        if sample_rate != 16000:
            logger.info("Resampling from %d Hz to 16000 Hz", sample_rate)
            resampler = torchaudio.transforms.Resample(sample_rate, 16000)
            waveform = resampler(waveform)
        
        # Convert to numpy
        audio_array = waveform.squeeze().numpy()
        
        logger.info("Audio loaded: %.2f seconds", len(audio_array) / 16000)
        
        return audio_array
    
    def transcribe(self, audio_path: str, return_confidence: bool = False) -> Dict:
        """
        Transcribe audio to text
        
        Args:
            audio_path: Path to audio file
            return_confidence: Whether to return confidence scores
            
        Returns:
            Dictionary with transcription results
        """
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        # Load audio
        audio_array = self.load_audio(audio_path)
        
        # Process audio
        logger.info("Processing audio...")
        inputs = self.processor(
            audio_array,
            sampling_rate=16000,
            return_tensors="pt"
        ).input_features.to(self.device)
        
        # Generate transcription
        logger.info("Generating transcription...")
        with torch.no_grad():
            generated_ids = self.model.generate(
                inputs,
                max_length=448,
                num_beams=5,
                temperature=0.0,
                return_dict_in_generate=True,
                output_scores=return_confidence
            )
        
        # Decode transcription
        transcription = self.processor.batch_decode(
            generated_ids.sequences,
            skip_special_tokens=True
        )[0]
        
        result = {
            'transcription': transcription.strip(),
            'audio_file': audio_path,
            'model_size': self.model_size,
            'language': 'es-MX',
            'duration_seconds': len(audio_array) / 16000,
            'timestamp': datetime.now().isoformat()
        }
        
        # Add confidence if requested
        if return_confidence and hasattr(generated_ids, 'sequences_scores'):
            confidence = torch.exp(generated_ids.sequences_scores[0]).item()
            result['confidence'] = float(confidence)
        
        logger.info("Transcription completed: %s", transcription[:100])
        
        return result
    
    def transcribe_batch(self, audio_paths: list, return_confidence: bool = False) -> list:
        """
        Transcribe multiple audio files
        
        Args:
            audio_paths: List of audio file paths
            return_confidence: Whether to return confidence scores
            
        Returns:
            List of transcription results
        """
        logger.info("Processing batch of %d audio files", len(audio_paths))
        
        results = []
        for i, audio_path in enumerate(audio_paths, 1):
            logger.info("Processing %d/%d: %s", i, len(audio_paths), audio_path)
            try:
                result = self.transcribe(audio_path, return_confidence)
                results.append(result)
            except Exception as e:
                logger.error("Failed to process %s: %s", audio_path, str(e))
                results.append({
                    'audio_file': audio_path,
                    'error': str(e),
                    'transcription': None
                })
        
        logger.info("Batch processing completed")
        return results
    
    def get_model_info(self) -> Dict:
        """Get information about loaded model"""
        if not self.is_loaded:
            return {'error': 'Model not loaded'}
        
        config = self.MODEL_CONFIGS[self.model_size]
        
        return {
            'model_size': self.model_size,
            'model_id': config['model_id'],
            'size_mb': config['size_mb'],
            'speed': config['speed'],
            'quality': config['quality'],
            'device': self.device,
            'language': 'Spanish (Mexico)',
            'is_loaded': self.is_loaded
        }


def main():
    """Main execution with CLI"""
    parser = argparse.ArgumentParser(
        description='AuraVoiceLite STT - Speech-to-Text Inference'
    )
    parser.add_argument(
        '--audio',
        type=str,
        required=True,
        help='Path to audio file (WAV, MP3, etc.)'
    )
    parser.add_argument(
        '--model',
        type=str,
        default='base',
        choices=['tiny', 'base', 'small', 'medium'],
        help='Whisper model size (default: base)'
    )
    parser.add_argument(
        '--confidence',
        action='store_true',
        help='Return confidence scores'
    )
    parser.add_argument(
        '--device',
        type=str,
        choices=['cpu', 'cuda'],
        help='Device to use (auto-detect if not specified)'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize engine
        engine = VoiceLiteSTT(model_size=args.model, device=args.device)
        
        # Show model info
        print("\n" + "=" * 80)
        print("AURA VOICELITE - SPEECH-TO-TEXT")
        print("=" * 80)
        config = engine.MODEL_CONFIGS[args.model]
        print(f"\nModelo: {args.model}")
        print(f"Tamaño: {config['size_mb']} MB")
        print(f"Velocidad: {config['speed']}")
        print(f"Calidad: {config['quality']}")
        print(f"Dispositivo: {engine.device}")
        print(f"Idioma: Español (México)")
        
        # Load model
        print(f"\nCargando modelo...")
        engine.load_model()
        print("Modelo cargado exitosamente")
        
        # Transcribe
        print(f"\nTranscribiendo: {args.audio}")
        result = engine.transcribe(args.audio, return_confidence=args.confidence)
        
        # Display results
        print("\n" + "=" * 80)
        print("RESULTADO")
        print("=" * 80)
        print(f"\nTranscripción: {result['transcription']}")
        print(f"Duración: {result['duration_seconds']:.2f} segundos")
        if 'confidence' in result:
            print(f"Confianza: {result['confidence']:.2%}")
        print("=" * 80)
        
        # Save to JSON
        output_path = args.audio.replace('.wav', '_transcription.json').replace('.mp3', '_transcription.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\nResultado guardado en: {output_path}")
        
    except Exception as e:
        logger.error("Execution failed: %s", str(e), exc_info=True)
        raise


if __name__ == "__main__":
    main()
