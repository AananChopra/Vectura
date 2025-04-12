# backend/MLMODEL/model_definitions.py
import torch.nn as nn
import torch

class LSTMCountryModel(nn.Module):
    def __init__(self, num_countries, embedding_dim=8, hidden_dim=64):
        super(LSTMCountryModel, self).__init__()
        self.embedding = nn.Embedding(num_countries, embedding_dim)
        self.lstm = nn.LSTM(input_size=1, hidden_size=hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim + embedding_dim, 1)

    def forward(self, country_ids, sequences):
        country_embed = self.embedding(country_ids)
        lstm_out, _ = self.lstm(sequences)
        last_output = lstm_out[:, -1, :]
        combined = torch.cat((last_output, country_embed), dim=1)
        return self.fc(combined)