---
title: "Logging Hyperparameters in Lightning"
tags: ['optimization', 'pytorch', 'tensorboard', 'lightning']
---

I've looked up how to use PyTorch Lightning to log hyperparameters into TensorBoard too many times now.
It is not hard, but it is a little confusing.
The primary API is to record the hyperparameters for reinstantiation of the model from checkpoints, and not for hyperparameter tuning.
So below is a simple working example on how to do it.

The key lines is to have 
- `default_hp_metric=True` in the `TensorBoardLogger` instantiation.
- `self.save_hyperparameters()` in the constructor of your LightningModule.
- `self.log("hp_metric", loss)` somewhere, e.g. in the test step.

The below example does logitistic regression on a toy dataset.
The input dimension and the learning rate are hyperparameters.
The test loss is logged as the hyperparameter evaluation metric.

```python
import sklearn.datasets
import torch
import torch.nn as nn
import torch.utils.data
import lightning


class LogRegModule(lightning.LightningModule):
  def __init__(self, learning_rate=1e-3, input_dim=20):
    super().__init__()
    # `self.save_hyperparameters()` will record hyperparameters to `self.hparams`
    # and store them in the checkpoint. It will only log them to tensorboard 
    # if the logger is set up to do so. See `default_hp_metric` below.
    self.save_hyperparameters()
    self.linear = nn.Linear(self.hparams.input_dim, 1)
    self.bcewithlogitsloss = nn.BCEWithLogitsLoss()

    def training_step(self, batch, batch_idx):
    x, y = batch
    logits = self.linear(x)
    loss = self.bcewithlogitsloss(logits, y.float().unsqueeze(1))
    self.log("nll/train", loss)
    return loss

  def test_step(self, batch, batch_idx):
    x, y = batch
    logits = self.linear(x)
    loss = self.bcewithlogitsloss(logits, y.float().unsqueeze(1))

    self.log("nll/test", loss)
    # you must log `hp_metric` to get the HPARAMS view in tensorboard
    self.log("hp_metric", loss)
    return loss

  def configure_optimizers(self):
    optimizer = torch.optim.Adam(self.parameters(), lr=self.hparams.learning_rate)
    return optimizer


def dataloaders():
  X, y = sklearn.datasets.make_classification(
    n_samples=5_000,
    n_features=20,
    n_classes=2,
  )
  X = torch.tensor(X, dtype=torch.float32)
  y = torch.tensor(y, dtype=torch.long)
  dataset = torch.utils.data.TensorDataset(X, y)
  train_dataset, test_dataset = torch.utils.data.random_split(dataset, [0.8, 0.2])
  train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=64, shuffle=True, num_workers=2)
  test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=64, num_workers=2)
  return train_loader, test_loader


if __name__ == "__main__":
  lightning.seed_everything(42) 
  train_loader, test_loader = dataloaders()
  model = LogRegModule(learning_rate=0.01, input_dim=20)
  # By setting `default_hp_metric=True`, we log the hyperparameters
  # already in the self.save_hyperparameters() call.
  # it is similar to  of like calling self.log('hp_metric', -1) in the constructor.
  # This is useful for hyperparameter tuning, since the hyperparameters
  # are logged even if the training is aborted and the test step is never reached.  
  logger = lightning.pytorch.TensorBoardLogger(
    "./toy_hparam_logs",
    default_hp_metric=True 
  )
  trainer = lightning.Trainer(
    max_epochs=5,
    logger=logger,
  )
  trainer.fit(model, train_dataloaders=train_loader)
  trainer.test(model, dataloaders=test_loader)
```