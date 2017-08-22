CRC Status Dash App
---

#### Description

Using Slurm data from CRC's compute cluster, the percent utilization over time is plotted. Plot updates every 5 minutes with new data being written every 15 minutes.

This was not meant as an administrative tool, but as an aesthetically pleasing plot for users to quickly gauge the activity on the various clusters at our center.

#### Software Resources

- [Dash](https://plot.ly/products/dash/) for plotting and updates on the fly
- [mLab](https://mlab.com/welcome/) and [PyMongo](http://api.mongodb.com/python/current/tutorial.html) for hosting and writing/reading to/from MongoDB
- [Heroku](https://www.heroku.com) for hosting the app

#### Data Collection

Data collection script is `mlab-instantaneous.py` and is triggered by a cron job.
