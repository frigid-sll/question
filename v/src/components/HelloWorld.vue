<template>
    <div id="Img">
        <input type="file" id="saveimage" style="position:absolute;left:20px;top:15px">
        <button @click="exit" class="btn-link slide" id="out" >退出登录</button>
        <button v-for="x in small" @click="addgoods(x)" class="btn btn-default a ">更改{{x.slice(1,x.length)}}</button><br>
        <button v-for="x in big" @click="addgoods(x)" class="btn btn-default a">更改{{x.slice(1,x.length)}}</button>
        
        <div id="amuse">
            <div class="box">
                <ul class="minbox">
                    <li v-for="value,index in small">
                        <img v-if="value!='a2'" :src="small_num[index]" width="100px" height="100px" :id="value">
                        <img v-if="value=='a2'" :src="small_num[index]" width="100px" height="100px" :id="value"  style="transform: rotate(180deg);">
                    </li>
                </ul>
                <ol class="maxbox">
                    <li v-for="value,index in big">
                        <img v-if="value!='a8'" :src="big_num[index]" width="200px" height="200px" :id="value">
                        <img v-if="value=='a8'" :src="big_num[index]" width="200px" height="200px" :id="value"  style="transform: rotate(180deg);">
                    </li>
                </ol>
            </div>
        </div>
        
    </div>
</template>
<script>
import Qs from 'qs'
export default {
    data(){
        return{
            small:['a1','a2','a3','a4','a5','a6'],
            small_num:["../../static/img/1.jpg","../../static/img/2.jpg","../../static/img/3.jpg",
                        "../../static/img/4.jpg","../../static/img/5.jpg","../../static/img/6.jpg"],
            big:['a7','a8','a9','a10','a11','a12'],
            big_num:["../../static/img/7.jpg","../../static/img/8.jpg","../../static/img/9.jpg",
                        "../../static/img/10.jpg","../../static/img/11.jpg","../../static/img/12.jpg"],
            }
    },
    methods:{
        addgoods:function (num) {
            
            //定义data值，方便于传送数据
            var data = new FormData();
            //1.从input框里获取图片
            var img = document.getElementById('saveimage').files[0];
            //2.将图片添加到Formdata中
            data.append('file',img,img.name);
            this.axios({
                    url:'/api/user/img/',
                    method:'post',
                    data:data,
                    headers:{'Content-Type':'multipart/form-data','X-CSRFToken': this.getCookie('csrftoken')}
                }).then((res)=>{
                    document.getElementById(num).src=res.data.img_url
                    this.timer = setTimeout(()=>{   
                            this.del_img() 
                        },100);
                    
            })
        },
        getCookie(name) {
                var value = '; ' + document.cookie;
                var parts = value.split('; ' + name + '=');
                if (parts.length === 2) return parts.pop().split(';').shift()
        },
        exit:function(){
            localStorage.clear()
            alert('退出成功')
            location.reload()
        },
        del_img:function(){
            this.axios.get('/api/user/del_img/').then((res)=>{
					if(res.data.code==200){
						alert('success')
					}
					}).catch(function(error){
						console.log(error)
					})
        }
    }
}
</script>

<style scoped>
    @import "../../static/css/style.css"; 
</style>