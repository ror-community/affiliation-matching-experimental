import os
import re
import fasttext
from unidecode import unidecode
from gensim.parsing.preprocessing import preprocess_string, strip_tags, strip_punctuation, strip_multiple_whitespaces

# Suppress erroneous error message on loading model that Meta never fixed
# https://github.com/facebookresearch/fastText/issues/1067
fasttext.FastText.eprint = lambda x: None


class Predictor():
	def __init__(self, path_to_model):
		self.model = os.path.join(path_to_model, 'model.bin')
		self.classifier = fasttext.load_model(self.model)

	def preprocess_text(self, text):
		custom_filters = [lambda x: x.lower(), strip_tags,
						  strip_punctuation, strip_multiple_whitespaces]
		return unidecode(' '.join(preprocess_string(text, custom_filters)))

	def predict_ror_id(self, affiliation, min_probability):
		affiliation = self.preprocess_text(affiliation)
		predicted_label = self.classifier.predict(affiliation, k=1, threshold=min_probability)
		if predicted_label and predicted_label[0] and predicted_label[1]:
			label, ratio = predicted_label[0][0], predicted_label[1][0]
			label = re.sub('__label__','', label)
			return label, ratio
		else:
			return None, None