# model.py

import torch
import torch.nn as nn
import torch.nn.functional as F

class TextClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, output_dim, dropout=0.5):
        super(TextClassifier, self).__init__()

        # Embedding layer
        self.embedding = nn.Embedding(vocab_size, embed_dim)

        # LSTM layer
        self.lstm = nn.LSTM(embed_dim, hidden_dim, num_layers=1, batch_first=True)

        # Fully connected layer
        self.fc = nn.Linear(hidden_dim, output_dim)

        # Dropout for regularization
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        # x: [batch_size, seq_length]
        embedded = self.embedding(x)               # [batch_size, seq_length, embed_dim]
        lstm_out, (ht, ct) = self.lstm(embedded)   # [batch_size, seq_length, hidden_dim]
        out = self.dropout(ht[-1])                 # [batch_size, hidden_dim]
        logits = self.fc(out)                      # [batch_size, output_dim]
        return logits
