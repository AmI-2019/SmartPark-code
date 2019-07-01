#ifndef SmartPark_h
#define SmartPark_h
#define SENS_NUM 12
#define MAX_STRIP 17
typedef struct 
{
	int v[SENS_NUM];
} vec;

class Sensor 
{
	public:
		Sensor(int pin);
		Sensor();
		bool isCrossed();
		bool rawIsCrossed();
		void sense();
		int getPin();
		bool getState();
		bool isSwitched();
		int assignedLeds[MAX_STRIP];
		bool wasChanged;
	private:
		bool _crossCheck(int value);
		int _pin;
		int _analogValue;
		bool _isCrossed;
		int _threshold;
		bool _lastState;
};
class Sequence
{
	public:
		Sequence();
		Sequence(int len);
		void fill(vec sequence);
		void setLen(int len);
		int getLen();
		vec getList();
	private:
		int _length;
		vec _sensors;
};

class Vehicle
{
	public:
		Vehicle();
		void assignSequence(vec seq);
		void assignFromSeq(Sequence seq);
		void assignLength(int len);
		void lastPosUpdate(int last_position);
		int getLastPos();
		int getNextPos();
		bool isFree();
		void reset();
		
	private:
		void _clear();
		int _lastPos;
		bool _isFree;
		Sequence _sequence;
};


int sensor_to_spot(int sensor);
int getlen(vec array);

#endif
