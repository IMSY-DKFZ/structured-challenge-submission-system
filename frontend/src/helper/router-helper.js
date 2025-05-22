import router from '../router/index'

export function getStaticUrl(location) {
    const { href } = router.resolve(location)
    return href
}