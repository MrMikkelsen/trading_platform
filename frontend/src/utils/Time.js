class Time {
    time = new Date("2017-06-30 15:30:00");

    clock = setInterval(() => {
        time.setTime(time.getTime() + 10000);
    }, 1000);
}