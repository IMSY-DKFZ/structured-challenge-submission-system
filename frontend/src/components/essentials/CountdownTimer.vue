<!-- CountdownTimer.vue -->
<template></template>
<script>
export default {
    data() {
        return {
            timerTarget: "", // Replace with your target time
            remainingTime: {
                days: 0,
                hours: 0,
                minutes: 0,
                seconds: 0,
            },
            isTargetReached: false,
            timerInterval: null,
        };
    },
    mounted() {
        this.calculateRemainingTime();
        this.timerInterval = setInterval(this.calculateRemainingTime, 1000); // Update every second
    },
    beforeDestroy() {
        clearInterval(this.timerInterval);
    },
    methods: {
        calculateRemainingTime() {
            const targetDate = new Date(this.timerTarget);
            const currentDate = new Date();

            if (currentDate < targetDate) {
                const timeDifference = targetDate - currentDate;
                const days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
                const hours = Math.floor((timeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((timeDifference % (1000 * 60)) / 1000);

                this.remainingTime = { days, hours, minutes, seconds };
                this.isTargetReached = false;
            } else {
                this.isTargetReached = true;
                clearInterval(this.timerInterval);
            }
        },
        updateTargetDate(newTargetDate) {
            this.timerTarget = newTargetDate;
            this.calculateRemainingTime(); // Recalculate remaining time with the new target date
        },
    },
};
</script>

