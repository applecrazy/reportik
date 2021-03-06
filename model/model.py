import os
import re

import numpy as np
import tensorflow as tf
import keras

from loader import DataManager
import seq2seq
import utils


class NewsSummarizationModel:
    model = None
    batch_size = None
    data = None
    text_replacements = {
        'U. S.': 'US',
        'U. K.': 'UK',
        'Sen.': 'Sen'
    }

    def __init__(self, manager: DataManager, batch_size=32):
        """
        Create a new NewsSummarizationModel instance.
        :param manager: A fully-configured DataManager with data loaded.
        :param batch_size: The batch size of the training loop.
        """
        self.data = manager
        self.batch_size = batch_size

    def build_model(self, latent_dim=20, depth=4):
        """
        Create and compile a AttentionSeq2Seq model with the configured parameters.
        :param latent_dim: The dimension of the hidden state of the encoder.
        :param depth: The number of cells inside the encoder and decoder.
        """
        print('[INFO] Compiling model...')
        self.model = seq2seq.AttentionSeq2Seq(
            input_dim=self.data.embedding_size,
            input_length=len(self.data.train_documents[0]),
            hidden_dim=latent_dim,
            output_length=len(self.data.train_summaries[0]),
            output_dim=self.data.embedding_size,
            depth=depth
        )

        self.model.compile(
            loss='mse',
            optimizer='adam',
            metrics=['acc']
        )
        print('[INFO] Done compiling model.')

    def train(self, epochs=1):
        """
        Train the model for the specified number of epochs.
        build_model() must be run before this function.
        :param epochs: The number of epochs to train for.
        """
        print(f'[INFO] Commencing training for {epochs} epochs...')
        cb = keras.callbacks.TensorBoard()
        self.model.fit_generator(
            self.data.generator(self.batch_size),
            epochs=epochs,
            steps_per_epoch=len(self.data.train_documents) // self.batch_size,
            validation_data=self.data.generator(self.batch_size, gen_type='val'),
            validation_steps=len(self.data.val_documents) // self.batch_size,
            callbacks=[cb]
        )
        print('[INFO] Training completed.')

    def plot_model(self, image_path='model.png'):
        """
        Use Keras utilities to create a graph of the model graph.
        :param image_path: The path where to save the image of the model graph.
        """
        tf.keras.utils.plot_model(self.model, to_file=image_path, show_shapes=True, show_layer_names=True)

    def evaluate(self):
        """
        Evaluate the performance of the model.
        build_model() must be run before this function.
        :return: Loss and accuracy metrics.
        """
        print('[INFO] Evaluating model...')
        metrics = self.model.evaluate_generator(
            self.data.generator(self.batch_size, gen_type='test'),
            steps=len(self.data.test_documents) // self.batch_size
        )
        print('[INFO] Done evaluating model.')
        return metrics

    def save(self, path, filename='model'):
        """
        Save the model's weights to the given path and filename.
        build_model() must be run before this function.
        :param path: The enclosing folder in which to save the weights.
        :param filename: The name of the weights file.
        """
        files = os.path.join(path, filename + '-seq2seq-attn-weights.h5')
        print(f'[INFO] Saving model at {files}...')
        self.model.save_weights(files)
        print('[INFO] Done saving weights.')

    def view_document_text(self, document):
        """
        Convert a sequence of document indices to text.
        :param document: An array of document word indices.
        :return: The decoded text of the document.
        """
        return self.data.document_tokenizer.sequences_to_texts([document])[0]

    def view_summary_text(self, summary):
        """
         Convert a sequence of summary indices to text.
        :param summary: An array of summary word indices.
        :return: The decoded text of the summary.
        """
        return self.data.summary_tokenizer.sequences_to_texts([summary])[0]

    def load(self, path):
        """
        Load saved model weights.
        build_model() must be run before this function.
        :param path: The full path (including filename) of the weights.
        """
        print('[INFO] Loading saved model weights...')
        self.model.load_weights(path)
        print('[INFO] Done loading saved weights.')

    def infer(self, document_text):
        """
        Summarize a source text.
        build_model() must be run before this function.
        :param document_text: The text of the input document.
        :return: Summary of the source document, as generated by the model.
        """
        print('[INFO] Beginning inference...')
        max_doc_len = len(self.data.train_documents[0])
        doc_seq = self.data.document_tokenizer.texts_to_sequences([utils.clean_text(document_text)])
        doc_seq = keras.preprocessing.sequence.pad_sequences(doc_seq, max_doc_len, truncating='post')
        doc_seq = np.squeeze(doc_seq)
        doc_seq = np.array([self.data.index_to_vec(x) for x in doc_seq])
        doc_seq = np.reshape(doc_seq, (1, -1, self.data.embedding_size))
        summ_seq = self.model.predict(doc_seq)
        summ_seq = np.reshape(summ_seq, (150, self.data.embedding_size))
        print(summ_seq.shape)
        words = []
        for x in summ_seq:
            words.append(np.squeeze(self.data.embeddings.similar_by_vector(x, topn=1))[0])
        print('[INFO] Completed inference.')
        return ' '.join(words)