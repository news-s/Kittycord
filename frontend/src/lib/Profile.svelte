<script>
    import { profile } from "../routes/app/stores";
</script>

<div class="profile-wrapper">
    <h1>{$profile.display_name}</h1>
    <p>{$profile.name}</p>
</div>

<style>
    .profile-wrapper {
        height: 70px;
        width: 272px;

        display: flex;
        flex-direction: column;

        padding: 10px;

        background-color: #888;

        position: absolute;
        top: 100%;
        transform: translateY(-100%);
    }

    p {
        font-size: 13px;
        color: #333;
    }
</style>