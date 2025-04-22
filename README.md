
# Pain Descriptor Auto-Tagger

*A linguist-built tool for metaphor analysis in pain discourse — powered by Python, grounded in theory, and fueled by mates 🧉  and metaphor.*

---

## 📅 What This Is
This project is a Python-based tagging tool that processes pain descriptors and automatically identifies metaphor types, experiential framing, intensity, and salience. It's designed for use in linguistic research, health communication, and clinical discourse analysis.

Developed by a linguist transitioning into tech, with a growing specialization in NLP and machine learning, this tool bridges metaphor theory and structured annotation to support the analysis of health-related language.

---

## 🧪 Why This Matters
Pain is complex. And how people *talk* about pain is often metaphorical. Expressions like:
- "It's like a monster creeping under my skin"
- "A volcano exploding in my chest"
- "A dull throb that won't stop"

...tell us more than just symptoms — they reveal experience, fear, emotion, embodiment.

This tool captures those metaphors, classifies them by type and intensity, and makes them easier to study, compare, and visualize.

---

## ⚙️ What It Does
Given a CSV file of pain descriptors, the script:
- Detects whether an expression is **metaphorical**, **a simile**, or **non-metaphorical**
- Tags **metaphor subtypes** (e.g. `violence_with_object`, `transformative_state`)
- Assigns **experience tags**: `sensory`, `affective`, `temporal`
- Highlights the **salient_experience** (which one dominates the framing)
- Estimates **intensity_level**: `low`, `medium`, or `high`

---

## 🔄 How It Works
The script uses keyword matching, regex, and stemming to:
- Match metaphorical patterns
- Parse known metaphor themes (defined in a taxonomy)
- Infer the experiential frame (what kind of "felt sense" it conveys)
- Detect similes via phrases like *"feels like"*, *"as if"*, etc.
- Prioritize affective content when relevant

You get a CSV output with these new columns:
- `metaphor_type`
- `metaphor_subtypes`
- `experience_tags`
- `salient_experience`
- `intensity_level`

---

## 📚 Usage
Make sure you have:
- A working Python 3 environment (ideally in a virtualenv)
- `pandas` and `nltk` installed
- Your input file: `pain_descriptors_categorized_updated.csv`

Run the script:
```bash
python pain_descriptor_auto_tagger.py
```

Output will be saved as:
```
pain_descriptors_final_tagged_all_layers.csv
```

---

## 🌐 Versión en Español

### 📅 ¿Qué es esto?
Una herramienta de etiquetado automático para descriptores de dolor con base en teoría de la metáfora conceptual. Construida, muchos mates 🧉 de por medio , en Python por una investigadora en lingüística, permite identificar tipos de metáforas, marcos experienciales e intensidad expresiva en relatos de dolor.

### 🧪 ¿Por qué importa?
Porque el dolor no solo se siente: se cuenta. Y la forma en que lo contamos suele ser metáforica. Esta herramienta permite analizar, categorizar y comparar esas expresiones para comprender mejor la experiencia humana del dolor.

### ⚙️ ¿Cómo funciona?
Procesa un archivo CSV con descripciones de dolor e identifica:
- Si hay metáforas o símiles
- El tipo de metáfora según una taxonomía
- Si el foco está en lo sensorial, afectivo o temporal
- Cuál de esos marcos es más saliente
- El nivel de intensidad percibida

Genera un archivo de salida listo para análisis, visualización o validación manual.

---

## 👤 Autoría
Este proyecto fue desarrollado por Stella Bullo, doctora en lingüística, investigadora en comunicación de la salud, y aprendiz autodidacta de Python. Actualmente en transición hacia la tecnología, con especial interés en NLP y aprendizaje automático aplicados a la comunicación en salud.

Metáforas, mate y metodología: todo está en la mezcla 🍜🚀
