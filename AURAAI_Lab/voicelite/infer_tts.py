"""
AuraVoiceLite - Text-to-Speech Inference
Production-grade TTS inference using Meta MMS-TTS for emergency voice responses.
Optimized for Spanish (Mexico) with natural prosody.

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
    from transformers import VitsModel, AutoTokenizer
except ImportError:
    print("Error: transformers library not installed.")
    print("Install with: pip install transformers torch torchaudio")
    exit(1)

# Paths
MODEL_CACHE_DIR = 'models/tts_cache'
CONFIG_PATH = 'models/tts_config.json'
INFERENCE_LOG = 'models/tts_inference.log'
OUTPUT_DIR = 'audio_output'

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


class VoiceLiteTTS:
    """Production TTS engine using Meta MMS-TTS"""
    
    # Emergency response templates
    EMERGENCY_TEMPLATES = {
        'bienvenida': [
            "Hola, soy AURA, tu asistente de emergencias. ¿En qué puedo ayudarte?",
            "Bienvenido a AURA Sentinel. Estoy aquí para ayudarte en cualquier emergencia."
        ],
        'calma': [
            "Mantén la calma. Respira profundo conmigo. Inhala... exhala...",
            "Todo va a estar bien. Vamos a respirar juntos. Inhala por cuatro segundos.",
            "Tranquilo, estoy aquí contigo. Vamos a calmarnos poco a poco."
        ],
        'instrucciones': [
            "Escucha con atención. Voy a darte instrucciones paso a paso.",
            "Muy bien. Ahora sigue estos pasos cuidadosamente.",
            "Perfecto. Te voy a guiar. Paso número uno:"
        ],
        'ubicacion': [
            "¿Puedes decirme tu ubicación exacta?",
            "Necesito que me digas dónde te encuentras.",
            "¿En qué colonia o calle estás ubicado?"
        ],
        'ayuda_camino': [
            "La ayuda está en camino. Mantén la calma.",
            "Los servicios de emergencia ya están en ruta hacia tu ubicación.",
            "Una ambulancia está llegando. Espera donde estás."
        ],
        'confirmacion': [
            "Entendido. Procesando tu información.",
            "Perfecto. Ya tengo tus datos.",
            "Recibido. Continuemos."
        ]
    }
    
    def __init__(self, device: Optional[str] = None):
        """
        Initialize TTS engine
        
        Args:
            device: Device to use ('cuda', 'cpu', or None for auto-detect)
        """
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.tokenizer = None
        self.is_loaded = False
        
        # Create output directory
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        logger.info("VoiceLite TTS initialized")
        logger.info("Device: %s", self.device)
    
    def load_model(self):
        """Load Meta MMS-TTS model for Spanish"""
        logger.info("Loading MMS-TTS model for Spanish...")
        
        model_id = "facebook/mms-tts-spa"  # Spanish TTS
        
        try:
            # Load tokenizer
            logger.info("Loading tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_id,
                cache_dir=MODEL_CACHE_DIR
            )
            
            # Load model
            logger.info("Loading model...")
            self.model = VitsModel.from_pretrained(
                model_id,
                cache_dir=MODEL_CACHE_DIR
            ).to(self.device)
            
            # Set to evaluation mode
            self.model.eval()
            
            self.is_loaded = True
            logger.info("Model loaded successfully")
            logger.info("Configured for Spanish (Mexico)")
            
        except Exception as e:
            logger.error("Failed to load model: %s", str(e))
            raise
    
    def synthesize(self, text: str, output_path: Optional[str] = None) -> Dict:
        """
        Synthesize speech from text
        
        Args:
            text: Text to synthesize
            output_path: Path to save audio (auto-generated if None)
            
        Returns:
            Dictionary with synthesis results
        """
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        logger.info("Synthesizing text: %s", text[:100])
        
        # Tokenize text
        inputs = self.tokenizer(text, return_tensors="pt").to(self.device)
        
        # Generate audio
        with torch.no_grad():
            output = self.model(**inputs)
        
        # Get waveform
        waveform = output.waveform.squeeze().cpu()
        
        # Generate output path if not provided
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(OUTPUT_DIR, f"tts_output_{timestamp}.wav")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        
        # Save audio
        logger.info("Saving audio to: %s", output_path)
        torchaudio.save(
            output_path,
            waveform.unsqueeze(0),
            sample_rate=self.model.config.sampling_rate
        )
        
        result = {
            'text': text,
            'output_file': output_path,
            'duration_seconds': len(waveform) / self.model.config.sampling_rate,
            'sample_rate': self.model.config.sampling_rate,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info("Synthesis completed: %.2f seconds", result['duration_seconds'])
        
        return result
    
    def synthesize_batch(self, texts: list, output_dir: Optional[str] = None) -> list:
        """
        Synthesize multiple texts
        
        Args:
            texts: List of texts to synthesize
            output_dir: Directory to save audio files
            
        Returns:
            List of synthesis results
        """
        logger.info("Processing batch of %d texts", len(texts))
        
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        results = []
        for i, text in enumerate(texts, 1):
            logger.info("Processing %d/%d", i, len(texts))
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = os.path.join(
                    output_dir or OUTPUT_DIR,
                    f"tts_batch_{i}_{timestamp}.wav"
                )
                result = self.synthesize(text, output_path)
                results.append(result)
            except Exception as e:
                logger.error("Failed to process text %d: %s", i, str(e))
                results.append({
                    'text': text,
                    'error': str(e),
                    'output_file': None
                })
        
        logger.info("Batch processing completed")
        return results
    
    def synthesize_emergency_response(self, response_type: str, 
                                      custom_text: Optional[str] = None) -> Dict:
        """
        Synthesize pre-defined emergency response
        
        Args:
            response_type: Type of emergency response
            custom_text: Custom text (uses template if None)
            
        Returns:
            Synthesis result
        """
        if response_type not in self.EMERGENCY_TEMPLATES:
            raise ValueError(
                f"Invalid response type. Choose from: {list(self.EMERGENCY_TEMPLATES.keys())}"
            )
        
        # Use custom text or select template
        if custom_text:
            text = custom_text
        else:
            import random
            text = random.choice(self.EMERGENCY_TEMPLATES[response_type])
        
        logger.info("Generating emergency response: %s", response_type)
        
        # Generate filename with type
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(OUTPUT_DIR, f"emergency_{response_type}_{timestamp}.wav")
        
        result = self.synthesize(text, output_path)
        result['response_type'] = response_type
        
        return result
    
    def get_model_info(self) -> Dict:
        """Get information about loaded model"""
        if not self.is_loaded:
            return {'error': 'Model not loaded'}
        
        return {
            'model_id': 'facebook/mms-tts-spa',
            'language': 'Spanish',
            'sample_rate': self.model.config.sampling_rate,
            'device': self.device,
            'is_loaded': self.is_loaded
        }


def main():
    """Main execution with CLI"""
    parser = argparse.ArgumentParser(
        description='AuraVoiceLite TTS - Text-to-Speech Inference'
    )
    parser.add_argument(
        '--text',
        type=str,
        help='Text to synthesize'
    )
    parser.add_argument(
        '--emergency',
        type=str,
        choices=['bienvenida', 'calma', 'instrucciones', 'ubicacion', 
                'ayuda_camino', 'confirmacion'],
        help='Generate emergency response template'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output audio file path (auto-generated if not specified)'
    )
    parser.add_argument(
        '--device',
        type=str,
        choices=['cpu', 'cuda'],
        help='Device to use (auto-detect if not specified)'
    )
    
    args = parser.parse_args()
    
    if not args.text and not args.emergency:
        parser.error("Either --text or --emergency must be specified")
    
    try:
        # Initialize engine
        engine = VoiceLiteTTS(device=args.device)
        
        # Show info
        print("\n" + "=" * 80)
        print("AURA VOICELITE - TEXT-TO-SPEECH")
        print("=" * 80)
        print(f"\nDispositivo: {engine.device}")
        print(f"Idioma: Español")
        print(f"Modelo: Meta MMS-TTS")
        
        # Load model
        print(f"\nCargando modelo...")
        engine.load_model()
        print("Modelo cargado exitosamente")
        
        # Synthesize
        if args.emergency:
            print(f"\nGenerando respuesta de emergencia: {args.emergency}")
            result = engine.synthesize_emergency_response(args.emergency)
        else:
            print(f"\nSintetizando: {args.text}")
            result = engine.synthesize(args.text, args.output)
        
        # Display results
        print("\n" + "=" * 80)
        print("RESULTADO")
        print("=" * 80)
        print(f"\nTexto: {result['text']}")
        print(f"Archivo de audio: {result['output_file']}")
        print(f"Duración: {result['duration_seconds']:.2f} segundos")
        print(f"Sample rate: {result['sample_rate']} Hz")
        print("=" * 80)
        
        # Save metadata
        metadata_path = result['output_file'].replace('.wav', '_metadata.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\nMetadata guardada en: {metadata_path}")
        
    except Exception as e:
        logger.error("Execution failed: %s", str(e), exc_info=True)
        raise


if __name__ == "__main__":
    main()
