
function BehaveData = loadBdaData(BdaList, framNum, BehavioralDelay)


fileNumRoi = length(BdaList);


eventNameList = [];
allTrialEvents                = cell(fileNumRoi,1);
for trialInd = 1:fileNumRoi
    usrData                    = load(fullfile(BdaList(trialInd).folder, BdaList(trialInd).name));
    allTrialEvents{trialInd}   = usrData.strEvent;
    for event_i = 1:length(allTrialEvents{trialInd})
        if isempty(eventNameList) || ~any(strcmpi(eventNameList, allTrialEvents{trialInd}{event_i}.Name))
            eventNameList{end+1} = extractEventstr(allTrialEvents{trialInd}{event_i}.Name);
        end
    end
end
% framNum = size(imagingData.samples,2);
for eventName_i = 1:length(eventNameList)
    BehaveData.(eventNameList{eventName_i}).indicator = zeros(fileNumRoi, framNum);
end

for trial_i = 1:fileNumRoi
    for m = 1:length(allTrialEvents{trial_i})
        eventname = lower(allTrialEvents{trial_i}{m}.Name);
        eventname = extractEventstr(eventname);
        if length(allTrialEvents{trial_i}{m}.tInd) ==2
            timeInd     = allTrialEvents{trial_i}{m}.tInd;
        else
            timeInd     = allTrialEvents{trial_i}{m}.TimeInd;
        end
        if isempty(timeInd)
            continue;
        end
        %             frameRateRatio=size(allTrialEvents{trial_i}{end}.Data,1)/size(eventDataArray,1);
        %                 frameRateRatio=18
        timeInd     = round((timeInd-BehavioralDelay)); % transfers to time of the two photon
        timeInd     = max(1,min(framNum,timeInd));
        % assign to vector
        BehaveData.(eventname).indicator(trial_i, timeInd(1):timeInd(2)) = 1;
        BehaveData.(eventname).eventTimeStamps{trial_i} = timeInd;
    end
end
NAMES = fieldnames(BehaveData);
for name_i  =1:length(NAMES)
    [I,~] = find(BehaveData.(NAMES{name_i}).indicator);
    BehaveData.(NAMES{name_i}).indicatorPerTrial = zeros(fileNumRoi,1);
    BehaveData.(NAMES{name_i}).indicatorPerTrial(unique(I)) = 1;
end



for event_i = 1:length(eventNameList)
    switch eventNameList{event_i}
        case {'failure', 'success'}
            BehaveData.(eventNameList{event_i})=BehaveData.(eventNameList{event_i})(:);
        otherwise
            BehaveData.(eventNameList{event_i}).indicator=BehaveData.(eventNameList{event_i}).indicator(:, :);
    end
end








