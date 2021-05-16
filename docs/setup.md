# Setup

Setting up the cli requires the following dependencies for some of the tasks
- `chromedriver` for browser automation

## Notes
- On Mac, you need to allow `chromedriver` to execute without a certification, using the command:
```bash
xattr -d com.apple.quarantine $(which chromedriver)
```