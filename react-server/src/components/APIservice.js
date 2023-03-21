

export default class APIService {
    static UpdateUeser(id, username) {
        fetch('http://127.0.0.1:5000/user', {
            'method': 'PUT',
            headers: {
                'Contenty-Type': 'application/json'
            }
        })
    }
}