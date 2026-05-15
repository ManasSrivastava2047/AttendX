from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import io
import librosa
import streamlit as st


@st.cache_resource
def load_voice_encoder():
    encoder = VoiceEncoder()
    return encoder


def get_voice_embeddings(audio_bytes):
    try:
        encoder = load_voice_encoder()
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)

        wav = preprocess_wav(audio)
        embedding = encoder.embed_utterance(wav)

        # ✅ FIX: correct conversion
        return embedding.tolist()

    except Exception as e:
        st.error(f"Error processing audio: {e}")
        return None


def identify_speaker(new_embeddings, candidate_dict, threshold=0.65):
    if new_embeddings is None or not candidate_dict:
        return None, 0.0

    # ✅ ensure numpy array
    new_embeddings = np.array(new_embeddings)

    best_sid = None
    best_score = -1.0

    for sid, candidate_embedding in candidate_dict.items():
        if candidate_embedding:
            candidate_embedding = np.array(candidate_embedding)

            # ✅ cosine similarity (better than raw dot)
            similarity = np.dot(new_embeddings, candidate_embedding) / (
                np.linalg.norm(new_embeddings) * np.linalg.norm(candidate_embedding)
            )

            if similarity > best_score:
                best_score = similarity
                best_sid = sid

    if best_score >= threshold:
        return best_sid, best_score

    return None, best_score


def process_bulk_audio(audio_bytes, candidate_dict, threshold=0.65):
    try:
        encoder = load_voice_encoder()
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)

        segments = librosa.effects.split(audio, top_db=30)
        identified_results = {}

        for start, end in segments:
            if (end - start) < sr * 0.5:
                continue

            segment_audio = audio[start:end]
            wav = preprocess_wav(segment_audio)

            embedding = encoder.embed_utterance(wav)

            # ✅ FIX: convert before passing
            sid, score = identify_speaker(embedding.tolist(), candidate_dict, threshold)

            if sid:
                if sid not in identified_results or score > identified_results[sid]:
                    identified_results[sid] = score

        return identified_results

    except Exception as e:
        st.error(f"Error processing bulk audio: {e}")
        return {}