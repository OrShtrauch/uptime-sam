<template>
        <a>{{ reserved }}</a>
</template>

<script>
// import { host, host_port } from "../main"

import { update } from 'lodash';

export default {
    props: {
        title: String
    }, 
    data() {
        return {
            reserved: "Free",
            // host: host,
            // host_port: host_port,
        }
    },
    mounted() {
        this.getData();
        setInterval(() => {
            this.getData();    
            console.log("updated")
        }, 70000)
    },
    methods: {
        getData() {
            const url = `http://127.0.0.1:7896/resource/${this.title}` //`http://${host}:${host_port}`;
            fetch(url)
                .then((response) => response.json())
                .then((data) => this.reserved = data.title)
        }
    }
}
</script>
