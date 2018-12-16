# Hacker News
A scrapper of https://news.ycombinator.com site

## Preinstall Requisites

- `docker==18.09.0`
- `docker-compose==1.23.2`

### Note

- Run `usermod -aG docker $USER`
- Reboot system to avoid using sudo every time when you run docker.

## Installation

### Production

```bash
git clone git://github.com/theBuzzyCoder/HackerNews.git HackerNews
cd HackerNews
bash ./system_setup/deploy-app
```

### Development Mode

```bash
git clone git://github.com/theBuzzyCoder/HackerNews.git HackerNews
cd HackerNews
bash ./system_setup/deploy-dev-mode
```

## Roadmap

### Achieved Milestone

- [x] HTML Downloader
- [x] Downloaded HTML Parser
- [x] Post Django model
- [x] List View to view the post
- [x] Detail View to view the post
- [x] Ability to delete post for user
- [x] Ability to display new posts as new and read post as not new
- [x] Need to write installer to setup database
- [x] Ability to view downloaded HTML files

### Upcoming Milestone

- [ ] Ability to store path of downloaded HTML files in database.
- [ ] Ability to pick stored HTML file from the file path
- [ ] User Model for users to access post
- [ ] Ability for user to login to portal
- [ ] Ability to create account
- [ ] Ability to reset password
- [ ] Ability to automate the new updating on button click
