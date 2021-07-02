<template>
    <div id="root" class="container">
        {{_path}}{{get_all_user}}
        <button @click="exit" class="btn-link slide" id="out" >退出登录</button><br>
        <ol v-if="!user_question_classify" id="user_catalogue">
            <input class="form-control" id="value" placeholder="请输入你要查询的人" v-model="seek_account">
            <button class="btn btn-success slide" id="seek" @click="get_seek">查询</button>
            <li v-for="x in all_user" v-if="!is_seek">
                <a @click="get_user_question_classify(x.account)" class="slide">{{x.account}}</a>
            </li>
            <a v-if="is_seek"  @click="get_user_question_classify(seek_res)" class="slide">{{seek_res}}</a>
        </ol>
        <ul v-if="user_question_classify">
            <li v-if="user_question_classify.length>0" v-for="x in user_question_classify">
                <a @click="get_user_question_catalogue(x)" class="slide">{{x}}</a>
            </li>
            <span v-if="user_question_classify.length<1">没有答题记录</span>
        </ul>
    </div>
</template>
<script>
import Qs from 'qs'
export default {
    data(){
        return{
            all_user:'',
            user_question_classify:'',
            account:'',
            sex:'',
            question_classify:'',
            seek_account:'',
            is_seek:false,
            seek_res:''
        }
    },
    computed:{
        _path:function(){    
            if(!localStorage.getItem("root")){
                this.$router.push({
                        path:localStorage.getItem("path"),
                    })
            }else{
                this.timer = setTimeout(()=>{   
                localStorage.setItem('path','/root') 
                },100);
                localStorage.setItem('account','root')
            }
            
        },
        get_all_user:function(){
            this.axios.get('/api/acquire/all_user/').then((res)=>{
					if(res.data.code==200){
						this.all_user=res.data.all_user
					}
					}).catch(function(error){
						console.log(error)
					})
        },
    },
    methods:{
        exit:function(){
            localStorage.clear()
            alert('退出成功')
            location.reload()
        },
        get_user_question_classify:function(account){
            this.account=account
            this.axios.post('/api/acquire/user_question_classify/',
                            Qs.stringify({  
                                account:this.account,
                            }),
                            {headers: {'X-CSRFToken': this.getCookie('csrftoken')}}
                            ).then((res)=>{
                                if(res.data.code==200){
                                    this.user_question_classify=res.data.user_question_classify
                                    this.sex=res.data.sex
                                    console.log(this.user_question_classify)
                                }else{
                                    alert('获取问题类型失败')
                                }
                            })
        },
        get_user_question_catalogue:function(question_classify){
            this.question_classify=question_classify
            console.log(this.question_classify)
            localStorage.setItem('account',this.account)
            localStorage.setItem('question_classify',this.question_classify)
            localStorage.setItem('sex',this.sex)
            this.$router.push({
                path:'/catalogue',
            })
        },
        getCookie(name) {
                var value = '; ' + document.cookie;
                var parts = value.split('; ' + name + '=');
                if (parts.length === 2) return parts.pop().split(';').shift()
        },
        get_seek:function(){
            var is_every_seek=false
            for(var i=0;i<this.all_user.length;i++){
                if(this.all_user[i].account==this.seek_account){
                    this.is_seek=true
                    is_every_seek=true
                    this.seek_res=this.seek_account
                    break
                }
            }
            if(!is_every_seek){
                    alert('无该人员')
                }
            this.seek_account=''
        }
    }
}
</script>

<style scoped>
    @import "../../static/css/root.css"; 
</style>