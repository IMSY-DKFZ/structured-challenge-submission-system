<!-- CountdownTimer.vue -->
<template></template>
<script>
export default {
  data() {
    return {
      timerStart: '',
      timerTarget: '', // Replace with your target time
      remainingTime: {
        days: 0,
        hours: 0,
        minutes: 0,
        seconds: 0,
      },
      isTargetReached: false,
      isCountdownActive: false,
      timerInterval: null,
    }
  },
  mounted() {
    this.calculateRemainingTime()
    this.timerInterval = setInterval(this.calculateRemainingTime, 1000) // Update every second
  },
  beforeUnmount() {
    clearInterval(this.timerInterval)
  },
  methods: {
    calculateRemainingTime() {
      if (!this.timerTarget) {
        this.isCountdownActive = false
        return
      }

      const targetDate = new Date(this.timerTarget)
      if (Number.isNaN(targetDate.getTime())) {
        this.isCountdownActive = false
        clearInterval(this.timerInterval)
        return
      }

      const startDate = this.timerStart ? new Date(this.timerStart) : null
      const hasValidStart = Boolean(startDate) && !Number.isNaN(startDate.getTime())
      const currentDate = new Date()

      const beforeStart = hasValidStart && currentDate < startDate
      const beforeTarget = currentDate < targetDate

      if (!beforeStart && beforeTarget) {
        const timeDifference = targetDate - currentDate
        const days = Math.floor(timeDifference / (1000 * 60 * 60 * 24))
        const hours = Math.floor((timeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
        const minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60))
        const seconds = Math.floor((timeDifference % (1000 * 60)) / 1000)

        this.remainingTime = { days, hours, minutes, seconds }
        this.isTargetReached = false
        this.isCountdownActive = true
      } else {
        this.isCountdownActive = false
        if (!beforeTarget) {
          this.isTargetReached = true
          clearInterval(this.timerInterval)
        } else {
          this.isTargetReached = false
          this.remainingTime = { days: 0, hours: 0, minutes: 0, seconds: 0 }
        }
      }
    },
    updateTargetDate(newTargetDate, newStartDate = null) {
      if (newStartDate) {
        this.timerStart = newStartDate
      }
      this.timerTarget = newTargetDate
      this.calculateRemainingTime() // Recalculate remaining time with the new target date
    },
  },
}
</script>
