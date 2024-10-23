import http from 'k6/http';

const baseUrl = 'http://localhost:8000';

export const options = {
  scenarios: {
    constant_request_rate: {
      executor: 'ramping-arrival-rate',
      startRate: 0,
      stages: [
        { target: 60000, duration: '20m' },
      ],
      preAllocatedVUs: 100,
      maxVUs: 200,
    },
  },
};


export default function() {
  http.request('POST', `${baseUrl}/user-register`, {'username': 'user', 'name': 'User Name', 'birthdate': '1990-01-01T00:00:00', 'password': 'pass'})
}
