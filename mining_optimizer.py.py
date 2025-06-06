import numpy as np
import random
import time
from datetime import datetime
import requests  # For API calls to mining pools

class CryptoMiningOptimizer:
    def __init__(self):
        # Initialize with default parameters
        self.hashrate_samples = []
        self.power_usage_samples = []
        self.temperature_samples = []
        self.profitability_samples = []
        
        # Thresholds for decision making
        self.hashrate_threshold = 100  # MH/s
        self.temp_threshold = 75  # °C
        self.power_threshold = 800  # Watts
        self.profitability_threshold = 0.05  # BTC/day
        
        # Mining configuration
        self.current_overclock = 0  # Percentage
        self.current_power_limit = 100  # Percentage
        self.mining_mode = "balanced"  # balanced, performance, eco
        
        # Historical data storage
        self.historical_data = []
        self.decision_log = []
        
        # API endpoints (example)
        self.mining_pool_api = "https://api.miningpool.example/stats"
        self.price_api = "https://api.coingecko.com/api/v3/simple/price"
    
    def gather_mining_data(self):
        """Collect real-time mining data from APIs and local sensors"""
        try:
            # Simulated data - in reality you'd get this from your mining rig
            new_data = {
                'timestamp': datetime.now(),
                'hashrate': random.uniform(80, 120),  # MH/s
                'power_usage': random.uniform(700, 900),  # Watts
                'temperature': random.uniform(60, 85),  # °C
                'accepted_shares': random.randint(10, 30),
                'rejected_shares': random.randint(0, 3),
                'local_block_count': random.randint(0, 2)
            }
            
            # Get current crypto price
            response = requests.get(f"{self.price_api}?ids=bitcoin&vs_currencies=usd")
            btc_price = response.json()['bitcoin']['usd']
            
            # Calculate profitability
            profitability = (new_data['hashrate'] / 1000) * 0.0001  # Simplified profitability calculation
            new_data['profitability'] = profitability
            new_data['btc_price'] = btc_price
            
            self.hashrate_samples.append(new_data['hashrate'])
            self.power_usage_samples.append(new_data['power_usage'])
            self.temperature_samples.append(new_data['temperature'])
            self.profitability_samples.append(profitability)
            
            # Store complete data record
            self.historical_data.append(new_data)
            
            print(f"Gathered new data at {new_data['timestamp']}:")
            print(f"Hashrate: {new_data['hashrate']:.2f} MH/s")
            print(f"Power: {new_data['power_usage']:.2f} W")
            print(f"Temp: {new_data['temperature']:.2f}°C")
            print(f"Profitability: {profitability:.6f} BTC/day")
            
            return new_data
            
        except Exception as e:
            print(f"Error gathering data: {e}")
            return None
    
    def analyze_performance(self):
        """Analyze mining performance and detect patterns"""
        if not self.hashrate_samples:
            return None
            
        analysis = {
            'hashrate_mean': np.mean(self.hashrate_samples),
            'hashrate_std': np.std(self.hashrate_samples),
            'power_mean': np.mean(self.power_usage_samples),
            'temp_mean': np.mean(self.temperature_samples),
            'profitability_mean': np.mean(self.profitability_samples),
            'efficiency': np.mean([h/p for h,p in zip(self.hashrate_samples, self.power_usage_samples)]),
            'rejection_rate': sum([d['rejected_shares'] for d in self.historical_data[-10:]]) / 
                             sum([d['accepted_shares'] + d['rejected_shares'] for d in self.historical_data[-10:]])
        }
        
        print("\nPerformance Analysis:")
        print(f"Avg Hashrate: {analysis['hashrate_mean']:.2f} ± {analysis['hashrate_std']:.2f} MH/s")
        print(f"Avg Power Consumption: {analysis['power_mean']:.2f} W")
        print(f"Avg Temperature: {analysis['temp_mean']:.2f}°C")
        print(f"Avg Efficiency: {analysis['efficiency']:.4f} MH/s/W")
        print(f"Recent Rejection Rate: {analysis['rejection_rate']:.2%}")
        
        return analysis
    
    def make_optimization_decision(self, analysis):
        """Make optimization decisions based on performance analysis"""
        decisions = []
        
        # Hashrate decision
        if analysis['hashrate_mean'] < self.hashrate_threshold * 0.9:
            decisions.append("Increase hashrate by optimizing GPU settings")
        elif analysis['hashrate_mean'] > self.hashrate_threshold * 1.1:
            decisions.append("Hashrate above target - consider reducing power")
            
        # Temperature decision
        if analysis['temp_mean'] > self.temp_threshold:
            decisions.append("Temperature too high - increase cooling or reduce load")
            
        # Power efficiency decision
        if analysis['efficiency'] < 0.12:  # MH/s per Watt
            decisions.append("Low efficiency - adjust power limits or clock speeds")
            
        # Rejection rate decision
        if analysis['rejection_rate'] > 0.05:
            decisions.append("High rejection rate - check connection stability")
            
        # Profitability decision
        current_profitability = self.historical_data[-1]['profitability'] * self.historical_data[-1]['btc_price']
        if current_profitability < self.profitability_threshold:
            decisions.append("Profitability low - consider switching coins/algorithms")
            
        if not decisions:
            decisions.append("No optimization needed - maintain current settings")
            
        # Log the decision
        decision_record = {
            'timestamp': datetime.now(),
            'analysis': analysis,
            'decisions': decisions
        }
        self.decision_log.append(decision_record)
        
        print("\nOptimization Decisions:")
        for i, decision in enumerate(decisions, 1):
            print(f"{i}. {decision}")
            
        return decisions
    
    def implement_decisions(self, decisions):
        """Implement the optimization decisions (simulated)"""
        print("\nImplementing decisions:")
        
        for decision in decisions:
            if "increase hashrate" in decision.lower():
                if self.current_overclock < 15:  # Don't overclock too much
                    self.current_overclock += 5
                    print(f"Increasing overclock to {self.current_overclock}%")
                    
            elif "reduce power" in decision.lower():
                if self.current_power_limit > 80:
                    self.current_power_limit -= 5
                    print(f"Reducing power limit to {self.current_power_limit}%")
                    
            elif "temperature too high" in decision.lower():
                if self.mining_mode != "eco":
                    self.mining_mode = "balanced" if self.mining_mode == "performance" else "eco"
                    print(f"Switching to {self.mining_mode} mode to reduce heat")
                    
            elif "low efficiency" in decision.lower():
                # Find optimal balance between hashrate and power
                if self.current_overclock > 5:
                    self.current_overclock -= 2
                    self.current_power_limit -= 3
                    print(f"Adjusting for efficiency: OC {self.current_overclock}%, Power {self.current_power_limit}%")
                    
            elif "high rejection rate" in decision.lower():
                print("Resetting mining connection and checking pool stability")
                
            elif "switch coins" in decision.lower():
                print("Evaluating alternative coins for better profitability")
                
        print(f"\nCurrent configuration: {self.mining_mode} mode, "
              f"OC: {self.current_overclock}%, "
              f"Power Limit: {self.current_power_limit}%")
    
    def run_optimization_cycle(self):
        """Run one complete optimization cycle"""
        print("\n" + "="*50)
        print(f"Starting optimization cycle at {datetime.now()}")
        print("="*50)
        
        # Gather current mining data
        current_data = self.gather_mining_data()
        if not current_data:
            print("Failed to gather data - skipping cycle")
            return
            
        # Analyze performance
        analysis = self.analyze_performance()
        
        # Make optimization decisions
        decisions = self.make_optimization_decision(analysis)
        
        # Implement decisions
        self.implement_decisions(decisions)
        
        # Clean up old data (keep last 100 samples)
        if len(self.historical_data) > 100:
            self.historical_data = self.historical_data[-50:]
            self.hashrate_samples = self.hashrate_samples[-50:]
            self.power_usage_samples = self.power_usage_samples[-50:]
            self.temperature_samples = self.temperature_samples[-50:]
            self.profitability_samples = self.profitability_samples[-50:]
    
    def continuous_optimization(self, interval_minutes=15):
        """Run continuous optimization at specified intervals"""
        print("Starting continuous optimization process...")
        try:
            while True:
                self.run_optimization_cycle()
                print(f"\nWaiting {interval_minutes} minutes until next cycle...")
                time.sleep(interval_minutes * 60)
        except KeyboardInterrupt:
            print("\nOptimization process stopped by user")


# Example usage
if __name__ == "__main__":
    optimizer = CryptoMiningOptimizer()
    
    # Run a single optimization cycle for testing
    optimizer.run_optimization_cycle()
    
    # Or run continuous optimization (uncomment to use)
    # optimizer.continuous_optimization(interval_minutes=15)