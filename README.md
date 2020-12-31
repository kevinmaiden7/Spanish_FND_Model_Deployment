# Spanish_FND_Model_Deployment
Spanish Fake News Detection - Model Deployment Using Flask

### Install Libraries:

```bash
pip install -r requirements.txt
```

## API endpoints:

- For Spanish News: `/predict/spanish` Method: `POST`
- For English News: `/predict/english` Method: `POST`

JSON Body request:
```bash
{
  "text": "News"
}
```

JSON Body response:
```bash
{
  "fake": "True",
  "value": "1.0"
}
```
