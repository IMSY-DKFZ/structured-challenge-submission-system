<template>
    <div class="sticky-sidebar" :style="{ top: sidebarTop + 'px' }">
        <slot />
    </div>
</template>

<script>
export default {
    name: 'StickySidebar',
    data() {
        return {
            sidebarTop: 0,
        };
    },
    mounted() {
        window.addEventListener('scroll', this.handleScroll);
    },
    destroyed() {
        window.removeEventListener('scroll', this.handleScroll);
    },
    methods: {
        handleScroll() {
            const contentHeight = document.getElementById('content').offsetHeight;
            const sidebarHeight = this.$el.offsetHeight;
            const viewportHeight = window.innerHeight;

            // Calculate maximum scroll amount for the sidebar
            const maxScroll = contentHeight - sidebarHeight;

            // Calculate new top position for the sidebar
            let newTop = Math.min(maxScroll, window.scrollY);

            // Ensure sidebar stays within viewport when content is shorter
            if (contentHeight < viewportHeight) {
                newTop = 0;
            }

            this.sidebarTop = newTop + 15;
        },
    },
};
</script>

<style scoped>
.sticky-sidebar {
    position: sticky;
    top: 0;
    left: 0;
    width: 100%;

}
</style>
